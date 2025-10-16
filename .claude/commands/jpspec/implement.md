---
description: Execute implementation using specialized frontend and backend engineer agents with code review.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Execution Instructions

This command implements features using specialized engineering agents with integrated code review. Determine which implementation paths are needed based on the feature requirements.

### Phase 1: Implementation (Parallel Execution)

**IMPORTANT**: Launch applicable engineer agents in parallel for maximum efficiency.

#### Frontend Implementation (if UI/mobile components needed)

Use the Task tool to launch the **frontend-engineer** agent:

```
Implement the frontend for: [USER INPUT FEATURE]

Context:
[Include architecture, PRD, design specs, API contracts]

Implementation Requirements:

1. **Component Development**
   - Build React/React Native components
   - Implement proper TypeScript types
   - Follow component composition patterns
   - Ensure accessibility (WCAG 2.1 AA)

2. **State Management**
   - Choose appropriate state solution (local, Context, Zustand, TanStack Query)
   - Implement efficient data fetching
   - Handle loading and error states

3. **Styling and Responsiveness**
   - Implement responsive design
   - Use design system/tokens
   - Ensure cross-browser/platform compatibility

4. **Performance Optimization**
   - Code splitting and lazy loading
   - Proper memoization
   - Optimized rendering

5. **Testing**
   - Unit tests for components
   - Integration tests for user flows
   - Accessibility tests

Deliver production-ready frontend code with tests.
```

#### Backend Implementation (if API/services needed)

Use the Task tool to launch the **backend-engineer** agent:

```
Implement the backend for: [USER INPUT FEATURE]

Context:
[Include architecture, PRD, API specs, data models]

Implementation Requirements:

1. **API Development** (choose applicable)
   - RESTful endpoints with proper HTTP methods
   - GraphQL schema and resolvers
   - gRPC services and protocol buffers
   - CLI commands and interfaces

2. **Business Logic**
   - Implement core feature logic
   - Input validation and sanitization
   - Error handling and logging
   - Transaction management

3. **Database Integration**
   - Data models and migrations
   - Efficient queries with proper indexing
   - Connection pooling
   - Data validation

4. **Security**
   - Authentication and authorization
   - Input validation
   - SQL/NoSQL injection prevention
   - Secure secret management

5. **Testing**
   - Unit tests for business logic
   - Integration tests for APIs
   - Database tests

Choose language: Go, TypeScript/Node.js, or Python based on architecture decisions.
Deliver production-ready backend code with tests.
```

#### AI/ML Implementation (if ML components needed)

Use the Task tool to launch the **ai-ml-engineer** agent:

```
Implement AI/ML components for: [USER INPUT FEATURE]

Context:
[Include model requirements, data sources, performance targets]

Implementation Requirements:

1. **Model Development**
   - Training pipeline implementation
   - Feature engineering
   - Model evaluation and validation

2. **MLOps Infrastructure**
   - Experiment tracking (MLflow)
   - Model versioning
   - Training automation

3. **Model Deployment**
   - Inference service implementation
   - Model optimization (quantization, pruning)
   - Scalable serving architecture

4. **Monitoring**
   - Performance metrics
   - Data drift detection
   - Model quality tracking

Deliver production-ready ML system with monitoring.
```

### Phase 2: Code Review (Sequential after implementation)

#### Frontend Code Review

After frontend implementation, use the Task tool to launch the **frontend-code-reviewer** agent:

```
Review the frontend implementation for: [USER INPUT FEATURE]

Code to review:
[PASTE FRONTEND CODE FROM PHASE 1]

Conduct comprehensive review covering:

1. **Functionality**: Correctness, edge cases, error handling
2. **Performance**: Re-renders, bundle size, runtime performance
3. **Accessibility**: WCAG compliance, keyboard navigation, screen readers
4. **Code Quality**: Readability, maintainability, TypeScript types
5. **Testing**: Coverage, test quality
6. **Security**: XSS prevention, input validation

Provide categorized feedback:
- Critical (must fix before merge)
- High (should fix before merge)
- Medium (address soon)
- Low (nice to have)

Include specific, actionable suggestions.
```

#### Backend Code Review

After backend implementation, use the Task tool to launch the **backend-code-reviewer** agent:

```
Review the backend implementation for: [USER INPUT FEATURE]

Code to review:
[PASTE BACKEND CODE FROM PHASE 1]

Conduct comprehensive review covering:

1. **Security**: Authentication, authorization, injection prevention, secrets
2. **Performance**: Query optimization, scalability, resource management
3. **Code Quality**: Readability, error handling, type safety
4. **API Design**: RESTful/GraphQL patterns, error responses
5. **Database**: Schema design, migrations, query efficiency
6. **Testing**: Coverage, integration tests, edge cases

Provide categorized feedback:
- Critical (block merge)
- High (fix before merge)
- Medium (address soon)
- Low (nice to have)

Include specific, actionable suggestions with examples.
```

### Phase 3: Iteration and Integration

1. **Address Review Feedback**
   - Fix critical and high-priority issues
   - Re-review if significant changes made

2. **Integration Testing**
   - Verify frontend-backend integration
   - Test complete user workflows
   - Validate API contracts

3. **Documentation**
   - Update API documentation
   - Add code comments for complex logic
   - Document configuration and deployment

### Deliverables

- Fully implemented, reviewed code
- Comprehensive test suites
- Code review reports with resolution status
- Integration documentation
- Deployment-ready artifacts
