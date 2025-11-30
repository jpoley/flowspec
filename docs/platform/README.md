# Platform Design Documents

This directory contains platform and infrastructure design documents.

## Purpose

Platform design documents define the technical infrastructure, deployment, and operational aspects:
- **Infrastructure**: Cloud resources, Kubernetes manifests, IaC code
- **Deployment**: CI/CD pipelines, release processes
- **Observability**: Monitoring, logging, alerting strategies
- **Security**: Authentication, authorization, secrets management
- **Scalability**: Performance targets, scaling strategies

## Structure

Each platform design document is named `platform-{feature-name}.md` or organized by category.

## Usage

Platform designs are created by the `/jpspec:plan` workflow (Platform Engineer agent):

```bash
/jpspec:plan
```

These documents complement ADRs by focusing on operational and infrastructure concerns.

## Related Workflows

- **Created By**: `/jpspec:plan` workflow
- **Used By**: `/jpspec:implement` and `/jpspec:operate` workflows
- **Related**: See ADRs in `docs/adr/` for architectural decisions
