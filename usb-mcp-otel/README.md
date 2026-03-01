# USB-MCP-OTEL

A standardized OpenTelemetry (OTel) wrapper designed for the **USB Enterprise Platform Team**. This library provides a consistent way to implement tracing and metrics across all Python services, with built-in support for **FastMCP** servers.

## 🚀 Features

* **Zero-Config OTel**: Standardized configuration for enterprise OTLP exporters.
* **Modular Design**: Use the core telemetry wrapper standalone or with FastMCP.
* **Automated Tracing**: Middleware and decorators that capture tool calls, resources, and prompts automatically.
* **Fail-Safe**: Gracefully handles missing dependencies if only core features are needed.

---

## 📦 Installation

This library is modular. Choose the installation that fits your environment:

### 1. Core Only (Standalone)
Best for scripts or non-MCP services that just need standardized OTel setup.
```bash
pip install usb-mcp-otel