# GPG Signing for Agent Commits

This guide covers GPG signing for flowspec agent commits, enabling cryptographic distinction between human and agent work.

## Overview

Flowspec can generate and manage a GPG key specifically for agent-initiated commits. This provides:

- **Cryptographic verification**: Distinguish agent commits from human commits
- **Audit trail**: Verify commit authenticity with `git log --show-signature`
- **SLSA compliance**: Required for SLSA L2+ compliance in regulated pipelines
- **Supply chain integrity**: Align with kybernesis supply chain work

## Quick Start

### Initial Setup

Generate a GPG key and configure git signing:

```bash
flowspec gpg setup
```

This will:
1. Generate a 4096-bit RSA GPG key
2. Store the private key securely in your system keyring
3. Configure git to sign commits with this key
4. Display the key fingerprint for verification

### Check Status

View GPG signing configuration:

```bash
flowspec gpg status
```

Shows:
- GPG key fingerprint and details
- Git signing configuration
- Key expiration status (if applicable)

### Verify Signed Commits

After setup, all flowspec-initiated commits will be signed:

```bash
git log --show-signature
```

You'll see:
```
commit abc123...
gpg: Signature made Thu 03 Apr 2026 12:34:56 PM UTC
gpg:                using RSA key FINGERPRINT
gpg: Good signature from "Flowspec Agent <flowspec-agent@localhost>"
```

## Key Management

### Custom Key Identity

Generate a key with custom name and email:

```bash
flowspec gpg setup \
  --name "My Project Bot" \
  --email "bot@myproject.com"
```

### Key Rotation

Rotate your GPG key (recommended annually or after security incidents):

```bash
flowspec gpg rotate
```

This will:
1. Generate a new GPG key
2. Revoke the old key
3. Update git configuration to use the new key
4. Store the new key in the system keyring

**Important**: After rotation, old commits remain signed with the old key. The old key is revoked but still verifies historical signatures.

### Key Rotation Schedule

**Recommended rotation schedule**:
- **Annual rotation**: Rotate keys yearly as a security best practice
- **After incidents**: Rotate immediately if key compromise is suspected
- **Team changes**: Rotate when agent operators change

**Automated rotation** (optional):

Add to your CI/CD pipeline or cron:

```bash
# Rotate key every 365 days
flowspec gpg rotate --yes
```

### Export Public Key

Share your agent's public key so others can verify signatures:

```bash
# Export to file
flowspec gpg export --output agent-public-key.asc

# Or print to stdout
flowspec gpg export
```

Others can import the public key with:

```bash
gpg --import agent-public-key.asc
```

## Integration with Telemetry

When telemetry is enabled, the GPG key fingerprint is automatically included in telemetry events for provenance tracking.

View telemetry with GPG info:

```bash
flowspec telemetry view
```

Export telemetry for audit:

```bash
flowspec telemetry export --output telemetry-audit.json
```

The exported JSON includes:
- `gpg_fingerprint`: Full 40-character fingerprint
- `gpg_key_id`: Short 16-character key ID

## Security Considerations

### Key Storage

The private GPG key is stored in your system's secure keyring:

- **macOS**: Keychain
- **Linux**: Secret Service (GNOME Keyring, KWallet)
- **Windows**: Windows Credential Manager

The key is stored with:
- Service: `flowspec-agent-gpg`
- Username: `agent-key`

### Passphrase Protection

By default, flowspec generates keys **without passphrases** for automated signing. This is suitable for:

- Local development environments
- Trusted CI/CD runners
- Isolated agent execution environments

**For enhanced security** in shared environments, consider:
- Using hardware security keys (YubiKey, etc.)
- Implementing GPG agent with timed passphrase caching
- Running flowspec in isolated containers/VMs

### Key Compromise Response

If you suspect key compromise:

1. **Rotate immediately**:
   ```bash
   flowspec gpg rotate --yes
   ```

2. **Revoke the old key**:
   The rotation process automatically revokes the old key, but you can also manually revoke:
   ```bash
   gpg --gen-revoke <old-fingerprint>
   ```

3. **Distribute revocation certificate**:
   Upload the revoked key to public keyservers:
   ```bash
   gpg --send-keys <old-fingerprint>
   ```

4. **Audit commit history**:
   Review commits signed with the compromised key:
   ```bash
   git log --show-signature --grep-signed-by=<old-fingerprint>
   ```

## Advanced Usage

### Multiple Projects

Each project can have its own GPG key, or you can share one key across projects.

**Per-project keys** (recommended for isolation):

```bash
cd project-a
flowspec gpg setup --name "Project A Agent"

cd ../project-b
flowspec gpg setup --name "Project B Agent"
```

**Shared key** across projects:

1. Set up in one project:
   ```bash
   cd project-a
   flowspec gpg setup
   ```

2. Export and import in other projects:
   ```bash
   cd ../project-b
   # The key is already in your system keyring, just configure git:
   flowspec gpg status  # Shows the key is available
   ```

### Git Signature Verification

Configure git to require signature verification:

```bash
# Require signed commits on push
git config --local commit.gpgsign true

# Require signed tags
git config --local tag.gpgsign true

# Verify signatures on merge
git config --local merge.verifySignatures true
```

### Disable Signing Temporarily

To temporarily disable GPG signing:

```bash
# Disable commit signing
git config --local commit.gpgsign false

# Re-enable
git config --local commit.gpgsign true
```

## Troubleshooting

### "GPG command not found"

Install GPG on your system:

```bash
# Ubuntu/Debian
sudo apt install gnupg

# macOS
brew install gnupg

# Windows
# Download from: https://gpg4win.org/
```

### "Failed to sign the data"

This usually means GPG can't find your key. Check:

1. Verify key exists:
   ```bash
   flowspec gpg status
   ```

2. Import the key if needed:
   ```bash
   flowspec gpg setup --force
   ```

3. Check git configuration:
   ```bash
   git config --get user.signingkey
   git config --get commit.gpgsign
   ```

### "No secret key"

The private key is not in your GPG keyring. Reimport it:

```bash
# The key is stored in your system keyring
# Flowspec can reimport it:
flowspec gpg setup --force
```

### Signature Verification Fails

If `git log --show-signature` shows "BAD signature":

1. Check if the key was rotated
2. Import the current public key
3. Verify the fingerprint matches:
   ```bash
   flowspec gpg status
   ```

## Reference

### CLI Commands

| Command | Description |
|---------|-------------|
| `flowspec gpg setup` | Generate and configure GPG signing |
| `flowspec gpg status` | Show GPG signing status |
| `flowspec gpg rotate` | Rotate GPG key (revoke old, generate new) |
| `flowspec gpg export` | Export public key |

### Configuration Files

| Location | Purpose |
|----------|---------|
| System keyring | Private key storage |
| `.git/config` | Git signing configuration |
| `~/.gnupg/` | GPG keyring (local keys) |

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `GPG_TTY` | Terminal for GPG prompts (set to `$(tty)`) |
| `GNUPGHOME` | Override GPG home directory |

## See Also

- [Telemetry Guide](telemetry.md) - View GPG fingerprints in telemetry
- [SLSA Compliance](../reference/slsa-compliance.md) - Supply chain security
- [Git Signing Documentation](https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work) - Official git docs
