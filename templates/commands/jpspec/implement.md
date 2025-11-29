---
mode: agent
description: Execute implementation using specialized frontend and backend engineer agents with code review.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

This command executes the implementation workflow using multiple specialized engineering agents:

1. **Frontend Engineer Agent**: React or mobile development
   - Implements user interfaces using React or mobile frameworks
   - Follows UI/UX best practices
   - Ensures responsive and accessible designs
   - Implements client-side state management

2. **Frontend Code Reviewer Agent**: Expert reviews of React or mobile code
   - Conducts thorough code reviews of frontend implementations
   - Ensures code quality and best practices
   - Validates accessibility and performance
   - Provides actionable feedback

3. **Backend Engineer Agent**: CLI, API, middleware development
   - Implements backend services in Go, TypeScript, or Python
   - Develops CLI tools and command interfaces
   - Creates RESTful APIs and GraphQL endpoints
   - Implements middleware and business logic

4. **Backend Code Reviewer Agent**: Expert reviews of backend code
   - Reviews Go, TypeScript, and Python implementations
   - Ensures backend code quality and patterns
   - Validates API contracts and error handling
   - Checks performance and security considerations

5. **AI/ML Engineer Agent**: MLOps and AI engineering
   - Implements machine learning models and pipelines
   - Sets up MLOps infrastructure
   - Integrates AI/ML capabilities into applications
   - Ensures model versioning and monitoring

## Execution Flow

1. Parse user input and load implementation plan

2. **Frontend Implementation**:
   - Dispatch Frontend Engineer agent for UI/mobile development
   - Implement components, pages, and client logic
   - Dispatch Frontend Code Reviewer for quality assurance
   - Address review feedback

3. **Backend Implementation**:
   - Dispatch Backend Engineer agent for services and APIs
   - Implement CLI, API endpoints, and middleware
   - Dispatch Backend Code Reviewer for quality assurance
   - Address review feedback

4. **AI/ML Implementation** (if applicable):
   - Dispatch AI/ML Engineer agent
   - Implement ML models and pipelines
   - Set up MLOps infrastructure
   - Integrate with application systems

5. **Integration**:
   - Coordinate frontend and backend integration
   - Ensure end-to-end functionality
   - Validate complete feature implementation

6. **Output**:
   - Fully implemented feature code
   - Frontend and backend implementations
   - AI/ML components (if applicable)
   - Code review reports
   - Integration documentation

## Notes

- This command is a placeholder for future agent implementation
- Full engineer and reviewer agent integration will be completed in a future task
- Coordinates multiple specialist agents for comprehensive implementation
