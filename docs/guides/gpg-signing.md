# Agent GPG Commit Signing

This guide covers GPG commit signing for Flowspec agents, enabling cryptographic verification of agent-generated commits.

## Overview

Flowspec agents can generate their own GPG keys and sign commits to provide:
- **Cryptographic verification** of agent authorship
- **Non-repudiation** - proof that commits came from the agent
- **Trust chains** - link agent commits to their originating workflow
- **Audit trails** - track which agent made which changes

## Quick Start

### 1. Set Up GPG Signing

```bash
# Generate agent GPG key and configure git
flowspec gpg setup

# Output:
# ✓ GPG key generated
# ✓ Git configured for signing
#
# Fingerprint: A1B2C3D4E5F6A7B8C9D0E1F2A3B4C5D6E7F8A9B0
```

### 2. Verify Status

```bash
# Check GPG signing status
flowspec gpg status

# Output:
# ┌─ Agent GPG Signing Status ─┐
# │ Status          Configured  │
# │ Fingerprint     A1B2C3...   │
# │ Git Signing     Enabled     │
# └─────────────────────────────┘
```

### 3. Make Signed Commits

Once configured, all commits in the repository will be automatically signed by the agent:

```bash
git commit -m "feat: add new feature"
# Commit is automatically signed with agent's GPG key
```

## Commands

### `flowspec gpg setup`

Generate a new GPG key and configure git for commit signing.

```bash
# Set up in current repository
flowspec gpg setup

# Set up in specific repository
flowspec gpg setup --project-root /path/to/repo

# Force key regeneration
flowspec gpg setup --force
```

**What it does:**
1. Generates a 4096-bit RSA GPG key for "Flowspec Agent <agent@flowspec.local>"
2. Stores the key fingerprint in the system keyring
3. Configures local git settings:
   - `user.signingkey`: agent's GPG fingerprint
   - `commit.gpgsign`: true

### `flowspec gpg status`

Show current GPG signing configuration and status.

```bash
# Check status in current repository
flowspec gpg status

# Check status with detailed key information
flowspec gpg status --verbose

# Check status in specific repository
flowspec gpg status --project-root /path/to/repo
```

**Output includes:**
- Configuration status (configured/not configured)
- GPG key fingerprint
- Git signing status (enabled/disabled)
- Key creation date (with `--verbose`)
- Key identity (with `--verbose`)

### `flowspec gpg rotate`

Rotate the agent's GPG key (delete old key, generate new key).

```bash
# Rotate key (with confirmation prompt)
flowspec gpg rotate

# Rotate key without confirmation
flowspec gpg rotate --yes

# Rotate key for specific repository
flowspec gpg rotate --project-root /path/to/repo
```

**When to rotate:**
- Regular security practice (e.g., annually)
- Key compromise or suspected compromise
- Agent role change or re-provisioning
- Compliance requirements

**Warning:** Rotating a key does not re-sign historical commits. Old commits will still reference the old key fingerprint.

## Key Management

### Key Storage

- **GPG Keychain**: Keys are stored in the user's GPG keychain (`~/.gnupg/`)
- **Fingerprint**: The key fingerprint is stored in the system keyring for quick retrieval
- **Service Name**: `flowspec-agent-gpg`
- **Username**: `agent-key-fingerprint`

### Key Properties

```
Name:       Flowspec Agent
Email:      agent@flowspec.local
Type:       RSA
Length:     4096 bits
Expiration: None (does not expire)
```

### Security Considerations

1. **No Passphrase**: Agent keys are generated without a passphrase for automated signing
2. **Local Storage**: Keys are stored locally on the agent's system
3. **Per-User**: Each user account has its own agent key
4. **Repository Config**: Git signing is configured per-repository (local config)

## Git Configuration

GPG signing modifies local git configuration:

```bash
# View current configuration
git config --local user.signingkey
git config --local commit.gpgsign

# Manual configuration (not recommended - use 'flowspec gpg setup')
git config --local user.signingkey A1B2C3D4E5F6A7B8C9D0E1F2A3B4C5D6E7F8A9B0
git config --local commit.gpgsign true
```

## Checking GPG Status

Use the GPG-specific commands to inspect signing configuration:

```bash
# Check GPG signing status
flowspec gpg status

# Check with detailed key information
flowspec gpg status --verbose
```

## Verifying Signed Commits

### On GitHub

GitHub automatically verifies GPG-signed commits if the public key is uploaded:

1. Export the agent's public key:
   ```bash
   gpg --armor --export agent@flowspec.local > agent-key.asc
   ```

2. Add the key to GitHub:
   - Go to Settings → SSH and GPG keys → New GPG key
   - Paste the contents of `agent-key.asc`

3. Signed commits will show a "Verified" badge

### Locally

```bash
# Verify a signed commit
git log --show-signature -1

# Output:
# commit abc123def456...
# gpg: Signature made Thu Apr  3 12:34:56 2025 UTC
# gpg:                using RSA key A1B2C3D4E5F6A7B8C9D0...
# gpg: Good signature from "Flowspec Agent <agent@flowspec.local>"
```

## Key Rotation Workflow

Key rotation is important for security best practices:

```bash
# 1. Rotate the key
flowspec gpg rotate --yes

# Output:
# Old fingerprint: A1B2C3D4E5F6A7B8C9D0E1F2A3B4C5D6E7F8A9B0
# New fingerprint: F0E9D8C7B6A5F4E3D2C1B0A9F8E7D6C5B4A3F2E1

# 2. Export new public key
gpg --armor --export agent@flowspec.local > agent-key-new.asc

# 3. Update GitHub/GitLab with new key

# 4. (Optional) Sign a rotation commit
git commit --allow-empty -m "chore: rotate agent GPG key

Previous key: A1B2C3D4E5F6A7B8C9D0E1F2A3B4C5D6E7F8A9B0
New key:      F0E9D8C7B6A5F4E3D2C1B0A9F8E7D6C5B4A3F2E1

Signed-off-by: Flowspec Agent <agent@flowspec.local>"
```

### Rotation Schedule Recommendations

| Environment | Rotation Frequency | Rationale |
|-------------|-------------------|-----------|
| Development | Annually | Low risk, convenience |
| Staging | Quarterly | Moderate risk |
| Production | Monthly | High security requirements |
| Compromised | Immediately | Security incident |

## Troubleshooting

### GPG Not Found

```
Error: GPG not found. Please install gnupg.
```

**Solution:** Install GPG:
```bash
# Ubuntu/Debian
sudo apt install gnupg

# macOS
brew install gnupg

# Fedora/RHEL
sudo dnf install gnupg
```

### Git Not a Repository

```
Error: Not a git repository: /path/to/dir
```

**Solution:** Run `flowspec gpg setup` inside a git repository or specify `--project-root`:
```bash
cd /path/to/repo
flowspec gpg setup
```

### Commits Not Signed

**Symptoms:** Commits don't show "Verified" badge

**Diagnosis:**
```bash
# Check git config
git config --local commit.gpgsign
# Should output: true

git config --local user.signingkey
# Should output: your fingerprint

# Check GPG key exists
gpg --list-keys agent@flowspec.local
```

**Solution:**
```bash
# Reconfigure signing
flowspec gpg setup
```

### Keyring Access Error

```
Error: Failed to store fingerprint in keyring: ...
```

**Solution:** Ensure the system keyring is accessible. On Linux, you may need to install and configure a keyring backend:
```bash
sudo apt install gnome-keyring  # Ubuntu/Debian
# or
sudo dnf install gnome-keyring  # Fedora/RHEL
```

## Advanced Usage

### Multiple Repositories

Each repository requires its own `flowspec gpg setup` to enable signing. The same agent key is used across all repositories:

```bash
# Repository A
cd /path/to/repo-a
flowspec gpg setup

# Repository B
cd /path/to/repo-b
flowspec gpg setup

# Both repos use the same agent key, but each has local git config
```

### Disable Signing for a Repository

```bash
# Disable automatic signing
git config --local commit.gpgsign false

# Or unset the config
git config --local --unset commit.gpgsign
git config --local --unset user.signingkey
```

### Export Public Key for Distribution

```bash
# Export ASCII-armored public key
gpg --armor --export agent@flowspec.local > agent-public-key.asc

# Export binary public key
gpg --export agent@flowspec.local > agent-public-key.gpg

# Show fingerprint
gpg --fingerprint agent@flowspec.local
```

### Manual Key Deletion

```bash
# Delete secret and public key
gpg --delete-secret-and-public-key agent@flowspec.local

# Delete fingerprint from keyring
# (This is handled automatically by 'flowspec gpg rotate')
```

## Security Best Practices

1. **Regular Rotation**: Rotate agent keys on a schedule appropriate for your security requirements
2. **Key Backup**: Consider backing up the private key to a secure location (encrypted)
3. **Audit Logs**: Monitor telemetry for signing activity
4. **Access Control**: Restrict access to the agent's keyring and GPG directory
5. **Verification**: Regularly verify that commits are being signed correctly
6. **Incident Response**: Have a plan for key rotation in case of compromise

## Related Documentation

- [Telemetry Guide](./telemetry-guide.md) - Telemetry integration with GPG fingerprints
- [Security Workflow](./security-workflow.md) - Security scanning and compliance
- [Git Hooks](../reference/git-hooks.md) - Custom hooks for commit signing

## References

- [GPG Manual](https://www.gnupg.org/documentation/manuals/gnupg/)
- [Git Signing Documentation](https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work)
- [GitHub GPG Verification](https://docs.github.com/en/authentication/managing-commit-signature-verification)
