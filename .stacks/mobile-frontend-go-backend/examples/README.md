# Mobile Frontend + Go Backend - Example Files

This directory contains reference example files for the Mobile (React Native/Flutter) + Go stack.

## magefile.go - Build Automation

The `magefile.go` provides a comprehensive build automation system using [Mage](https://magefile.org/), a Make-like build tool written in Go.

### Installation

```bash
# Install Mage
go install github.com/magefile/mage@latest

# Copy magefile.go to your backend directory
cp magefile.go /path/to/your/backend/
cd /path/to/your/backend/
```

### Usage

```bash
# List all available targets
mage -l

# Build the application
mage build

# Run tests with coverage
mage test

# Run linting
mage lint

# Run security scans
mage security

# Generate SBOM
mage sbom

# Build production binary
mage buildrelease

# Run all CI checks
mage ci

# Clean build artifacts
mage clean
```

### Available Targets

| Target | Description |
|--------|-------------|
| `build` | Build the Go binary with version embedding (default) |
| `buildrelease` | Build optimized production binary with SHA256 digest |
| `test` | Run all tests with coverage report |
| `testshort` | Run short tests (excludes integration tests) |
| `lint` | Run golangci-lint |
| `format` | Format code with gofmt |
| `tidy` | Run go mod tidy |
| `verify` | Verify go.mod and go.sum are up to date |
| `security` | Run all security scans (SAST + SCA) |
| `securitysast` | Run gosec (static analysis) |
| `securitysca` | Run govulncheck (vulnerability scanning) |
| `sbom` | Generate CycloneDX SBOM (JSON + XML) |
| `installdeps` | Install Go dependencies |
| `clean` | Remove build artifacts |
| `all` | Run all quality checks |
| `ci` | Run all CI checks (used in GitHub Actions) |

### Configuration

Edit the constants at the top of `magefile.go` to match your project:

```go
const (
    binaryName    = "api"              // Your binary name
    mainPath      = "./cmd/api"        // Path to main.go
    outputDir     = "./bin"            // Output directory
    // ... other configuration
)
```

### GitHub Actions Integration

The magefile is designed to work seamlessly with GitHub Actions. See `../workflows/ci-cd.yml` for the complete CI/CD workflow that uses these Mage targets.

### Tools Auto-Installation

The magefile automatically installs required tools if they're not present:
- `golangci-lint` - Comprehensive Go linter
- `gosec` - Security scanner (SAST)
- `govulncheck` - Vulnerability scanner (SCA)
- `cyclonedx-gomod` - SBOM generator

### Version Embedding

The `build` and `buildrelease` targets automatically embed version information:

```go
// In your main.go:
package main

var (
    Version   = "dev"
    BuildTime = "unknown"
)

func main() {
    fmt.Printf("Version: %s\nBuilt: %s\n", Version, BuildTime)
    // ... rest of your code
}
```

The version is automatically determined from:
1. Git tags (`git describe --tags --always --dirty`)
2. Git commit hash (if no tags)
3. "dev" (if not in a git repository)

### Benefits Over Makefile

- **Written in Go**: No need to learn Make syntax
- **Cross-platform**: Works on Windows, macOS, Linux
- **Type safety**: Compile-time checking
- **IDE support**: Full autocomplete and navigation
- **Dependency management**: Automatic target dependencies
- **Error handling**: Better error messages

### Example CI Workflow

```yaml
- name: Install Mage
  run: go install github.com/magefile/mage@latest

- name: Run CI checks
  run: mage ci
```

This single command runs: lint, test, security scans, SBOM generation, and production build.
