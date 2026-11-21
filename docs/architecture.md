# Architecture diagrams

This document illustrates how security telemetry flows from Microsoft Power Platform, Dataverse and Copilot Studio into Microsoft Sentinel (hosted in the Microsoft Defender portal), how the read-only assessor evaluates baseline settings, and how response playbooks operate with Managed Identity.

All log table names, connectors and gaps reflect the verification in [docs/research/verification.md](research/verification.md).

## 1. Security telemetry flow into Microsoft Sentinel

```mermaid
flowchart LR
    subgraph Sources["Microsoft 365 and Power Platform workloads"]
        PPAdmin["Power Platform Admin, Power Apps, Connectors, DLP"]
        PAuto["Power Automate (CreateFlow, EditFlow, Sharing)"]
        DV["Dataverse (CRUD, Exports, Read logs, SAS, bot table)"]
        CS["Copilot Studio (Interactions, Plugins, Maker admin)"]
        Entra["Microsoft Entra ID (Sign-ins, Directory roles, Guests)"]
    end

    Purview["Microsoft Purview Audit (O365 Management API)"]

    subgraph Connectors["Sentinel CCF Data Connectors"]
        BizApps["Microsoft Business Applications 3.2.5+ (Admin, Automate, Dataverse)"]
        CopilotSol["Microsoft Copilot 3.0.2+ (Copilot connector)"]
        EntraConn["Microsoft Entra ID connector"]
        Agent365["Defender Security for AI (Agent 365 licence from 1 Jul 2026)"]
    end

    subgraph Tables["Log Analytics / Defender Portal Tables"]
        T1["PowerPlatformAdminActivity"]
        T2["PowerAutomateActivity"]
        T3["DataverseActivity"]
        T4["CopilotActivity"]
        T5["SigninLogs and AuditLogs"]
        T6["AgentsInfo (Defender XDR Advanced Hunting)"]
    end

    subgraph SOC["Microsoft Sentinel in Defender Portal"]
        Rules["OOB + Custom Analytics Rules"]
        Hunt["Proactive Hunting Queries"]
        WB["Power Platform Security Posture Workbook"]
        PB["Logic Apps Playbooks (Managed Identity)"]
    end

    PPAdmin --> Purview
    PAuto --> Purview
    DV --> Purview
    CS -->|"Interactions and plugins"| Purview
    CS -.->|"No documented Sentinel admin table; audit Dataverse bot table"| DV

    Purview --> BizApps
    Purview --> CopilotSol
    Entra --> EntraConn
    CS -->|"Inventory and runtime protection"| Agent365

    BizApps --> T1
    BizApps --> T2
    BizApps --> T3
    CopilotSol --> T4
    EntraConn --> T5
    Agent365 --> T6

    T1 --> Rules
    T2 --> Rules
    T3 --> Rules
    T4 --> Rules
    T5 --> Rules
    T1 --> WB
    T2 --> WB
    T3 --> WB
    T4 --> WB
    T5 --> WB
    T1 --> Hunt
    T2 --> Hunt
    T3 --> Hunt
    Rules --> PB
```

Key architectural notes:

- Do not ingest legacy tables (`PowerAppsActivity`, `PowerPlatformConnectorActivity`, `PowerPlatformDlpActivity`, `Dynamics365Activity`, `LLMActivity`, `AIAgentsInfo`).
- Microsoft Sentinel retires in the Azure portal after **31 March 2027** ([Microsoft Sentinel in the Microsoft Defender portal](https://learn.microsoft.com/en-us/azure/sentinel/microsoft-sentinel-defender-portal)).
- Because Microsoft does not document a Sentinel table for Purview Copilot Studio maker/admin events (`BotCreate`, `BotUpdateOperation-*`), auditing the Dataverse `bot` table (`DataverseActivity`) and blocking unauthenticated chat via DLP (`PP-CS-002`) close the gap.

## 2. Read-only baseline assessor data flow

```mermaid
flowchart TD
    Baseline["baseline/ YAML front matter (38 items: Tenant, Environment, Copilot Studio)"]
    CLI["pp-assessor CLI (Python 3.11+)"]

    subgraph Auth["Authentication and Guardrails"]
        Fixture["Offline JSON Fixture (No network calls)"]
        MSAL["MSAL TokenProvider (Delegated Device Code or App-Only SP)"]
        ScopeGuard["validate_read_only_scopes (Blocks ReadWrite and Write scopes)"]
        HttpGuard["ReadOnlyHttpClient (GET only; blocks POST, PUT, PATCH, DELETE)"]
    end

    Cache["CachingDataProvider (Per-run cache for 50+ environments)"]

    subgraph APIs["Read-Only Microsoft Admin APIs"]
        BAP["Power Platform BAP API (Tenant settings, DLP, Isolation, Envs, Groups, CMK)"]
        Graph["Microsoft Graph API (AuthorizationPolicy, Admin role assignments)"]
        DVApi["Dataverse Web API v9.2 (organizations audit/security, bots table)"]
    end

    Engine["Assessment Engine (34 Automated Checks + 4 Manual Items)"]

    subgraph Outputs["Assessment Outputs"]
        JSON["JSON Report (machine-readable)"]
        CSV["CSV Report (GRC and spreadsheets)"]
        MD["Markdown Report (ASD Blueprint style)"]
        DCR["Optional Logs Ingestion API -> PowerPlatformBaselineAssessor_CL"]
    end

    Baseline --> CLI
    CLI --> Fixture
    CLI --> MSAL
    MSAL --> ScopeGuard
    ScopeGuard --> HttpGuard
    Fixture --> Cache
    HttpGuard -->|"GET only"| BAP
    HttpGuard -->|"GET only"| Graph
    HttpGuard -->|"GET only"| DVApi
    BAP --> Cache
    Graph --> Cache
    DVApi --> Cache
    Cache --> Engine
    Engine --> JSON
    Engine --> CSV
    Engine --> MD
    JSON -.->|"Optional workbook feed"| DCR
```

## 3. Incident response playbook flow

```mermaid
flowchart LR
    Inc["High-Severity Sentinel Incident"]
    Auto["Sentinel Automation Rule (or Analyst Manual Trigger)"]

    subgraph Playbooks["Azure Logic Apps (System-Assigned Managed Identity)"]
        P1["PP-Notify-Admin-Team"]
        P2["PP-Disable-Risky-Flow"]
        P3["PP-Quarantine-Power-App"]
        P4["PP-Remove-User-Env-SecurityGroup"]
    end

    subgraph Targets["Target Control Planes"]
        Teams["Teams / SOC Admin Channel Webhook"]
        FlowAPI["Power Automate Management API (Stop Flow)"]
        AppsAPI["Power Apps Admin API (Set Quarantine State)"]
        GraphAPI["Microsoft Graph API (Remove Group Member + Revoke Sessions)"]
        SentinelComment["Microsoft Sentinel Incident Audit Comment"]
    end

    Inc --> Auto
    Auto --> P1
    Auto --> P2
    Auto --> P3
    Auto --> P4

    P1 --> Teams
    P2 --> FlowAPI
    P3 --> AppsAPI
    P4 --> GraphAPI

    P1 --> SentinelComment
    P2 --> SentinelComment
    P3 --> SentinelComment
    P4 --> SentinelComment
```

## References

- [Microsoft Sentinel solution for Microsoft Business Applications | Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/business-applications/solution-overview)
- [Microsoft Sentinel in the Microsoft Defender portal | Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/microsoft-sentinel-defender-portal)
- [Microsoft Power Platform API reference | Microsoft Learn](https://learn.microsoft.com/en-us/rest/api/power-platform/)
- [Automate threat response with playbooks in Microsoft Sentinel | Microsoft Learn](https://learn.microsoft.com/en-us/azure/sentinel/automation/automate-responses-with-playbooks)
- [ADR 0001: Assessor language and auth](adr/0001-assessor-language-and-auth.md)
