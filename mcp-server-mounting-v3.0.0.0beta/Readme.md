# Federated MCP Gateway Architecture

This repository contains a **Federated MCP (Model Context Protocol)** server setup. It utilizes a centralized Gateway pattern to provide a single entry point for MCP clients while delegating domain-specific logic to specialized sub-servers.

## 🏗️ Architecture Overview

The system is composed of a **Base Gateway Server** and multiple downstream **Sub-Servers**. This design allows for modularity, where each sub-server can be developed, deployed, and scaled independently.

### Key Components:
- **Base Gateway MCP Server**: The primary interface for [MCP Clients](https://modelcontextprotocol.io). It handles connection management, routing, and centralized authentication.
- **Azure AD (Entra ID)**: Provides identity services. The Base Server authenticates users and obtains a [JWT Access Token](https://learn.microsoft.com).
- **Hotel Booking Sub-Server**: Specialized server for managing hotel-related tools and resources.
- **Flight Booking Sub-Server**: Specialized server for managing flight-related tools and resources.

## 🔐 Security & Authentication Flow

1.  **Centralized Authentication**: The Base Server integrates with [Microsoft Entra ID](https://learn.microsoft.com) to authenticate the client.
2.  **Token Propagation**: Once authenticated, the JWT is propagated downstream to the sub-servers via the routing layer.
3.  **Granular Authorization**: Sub-servers perform their own [Authorization](https://learn.microsoft.com) by inspecting the token for:
    *   **App Roles**: (e.g., `Hotel.Admin`)
    *   **Scopes**: (e.g., `Flight.Read`)
    *   **Custom Claims**: Any adequate claims required for business logic.

## 🔄 Sequence Diagram

The following diagram illustrates the lifecycle of a request through the federated system:

```mermaid
sequenceDiagram
    participant Client as MCP Client (IDE/Desktop)
    participant Base as Base Gateway MCP Server
    participant AzureAD as Azure AD (Entra ID)
    participant Hotel as Hotel Booking Sub-Server
    participant Flight as Flight Booking Sub-Server

    Note over Client, Base: 1. Connection & Initial Auth
    Client->>Base: Connect & Request Tool/Resource
    Base->>AzureAD: Redirect for User Authentication
    AzureAD-->>Base: Return Access Token (JWT)
    
    Note over Base: 2. Routing & Propagation
    Base->>Base: Identify Target Sub-Server
    
    alt Request for Hotel Tool
        Base->>Hotel: Route Request + Propagate Access Token
        Note over Hotel: 3. Authorization (Sub-Server)
        Hotel->>Hotel: Validate App Roles / Scopes in Token
        Hotel-->>Base: Return Authorized Result
    else Request for Flight Tool
        Base->>Flight: Route Request + Propagate Access Token
        Note over Flight: 3. Authorization (Sub-Server)
        Flight->>Flight: Check Adequate Claims/Scopes
        Flight-->>Base: Return Authorized Result
    end

    Base-->>Client: Final Response
