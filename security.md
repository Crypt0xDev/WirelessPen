## 🔐 Security Policy

### 🛡️ Supported Versions

We actively maintain and provide security updates for the following versions of WirelessPen:

| Version | Supported          |
| ------- | ------------------ |
| 2.2.x   | ✅ Yes            |
| 2.1.x   | ⚠️ Limited Support |
| 2.0.x   | ❌ No             |
| < 2.0   | ❌ No             |

### 🚨 Reporting a Vulnerability

If you discover a security vulnerability in WirelessPen, please help us address it responsibly.

#### 📧 Contact Information
- **Email**: [crypt0xdev@protonmail.com](mailto:crypt0xdev@protonmail.com)
- **Subject**: `[SECURITY] WirelessPen Vulnerability Report`
- **PGP Key**: Available upon request for sensitive communications

#### 📋 What to Include

When reporting a security vulnerability, please provide:

1. **Description**: Clear description of the vulnerability
2. **Impact**: Potential impact and attack scenarios
3. **Reproduction**: Step-by-step reproduction instructions
4. **Environment**: OS, Python version, WirelessPen version
5. **Proof of Concept**: Code or commands demonstrating the issue (if safe)

#### ⏱️ Response Timeline

- **Initial Response**: Within 24-48 hours
- **Vulnerability Confirmation**: Within 5 business days
- **Fix Development**: 1-4 weeks depending on severity
- **Public Disclosure**: After fix is released and tested

#### 🎯 Severity Classification

**🔴 Critical (CVSS 9.0-10.0)**
- Remote code execution
- Privilege escalation to root
- Complete system compromise

**🟠 High (CVSS 7.0-8.9)**
- Local privilege escalation
- Sensitive data exposure
- Authentication bypass

**🟡 Medium (CVSS 4.0-6.9)**
- Information disclosure
- Denial of service
- Limited privilege escalation

**🟢 Low (CVSS 0.1-3.9)**
- Minor information leaks
- Low-impact security misconfigurations

#### 🏆 Recognition

Security researchers who responsibly disclose vulnerabilities will be:
- Credited in the security advisory
- Listed in our Hall of Fame (with permission)
- Mentioned in release notes
- Invited to test fixes before public release

### 🔒 Security Best Practices

#### For Users
- ✅ Always run WirelessPen with minimal required privileges
- ✅ Keep the framework updated to the latest version
- ✅ Use in isolated/virtualized environments when possible
- ✅ Follow responsible disclosure practices
- ❌ Don't use on networks without explicit permission
- ❌ Don't share captured handshakes or sensitive data

#### For Contributors
- ✅ Validate all user inputs
- ✅ Use secure coding practices
- ✅ Avoid hardcoded secrets or credentials
- ✅ Implement proper error handling
- ✅ Test with security scanners (bandit, safety)

### 📚 Security Resources

#### Framework Security Features
- **Input Validation**: All user inputs are validated and sanitized
- **Process Isolation**: Child processes run with limited privileges
- **Secure Defaults**: Conservative default configurations
- **Error Handling**: Detailed logging without sensitive data exposure

#### External Security Tools
- **Bandit**: Static security analysis for Python code
- **Safety**: Dependency vulnerability scanning
- **CodeQL**: Automated security testing in CI/CD
- **SAST**: Static Application Security Testing

### 🚫 Out of Scope

The following are generally considered out of scope for security reports:
- Issues requiring physical access to target devices
- Social engineering attacks against users
- Vulnerabilities in third-party dependencies (report to upstream)
- Issues in development/debug modes not intended for production
- Rate limiting or DoS against the framework itself

### 📖 Legal Considerations

**Important Notes:**
- WirelessPen is designed for authorized penetration testing only
- Users are responsible for complying with local laws and regulations
- The project maintainers are not responsible for misuse of the tool
- Security research should follow responsible disclosure principles

### 🔄 Security Updates

Security updates are distributed through:
- **GitHub Releases**: Tagged releases with security patches
- **GitHub Security Advisories**: Detailed vulnerability information
- **Email Notifications**: For critical vulnerabilities (opt-in)
- **Documentation Updates**: Security best practices and guides

### 📞 Emergency Contact

For urgent security matters requiring immediate attention:
- **Priority Email**: Mark subject with `[URGENT SECURITY]`
- **Response Time**: Within 12 hours for critical vulnerabilities
- **Escalation**: If no response within 48 hours, contact via GitHub issues

---

**Remember: Security is a shared responsibility. Help us keep WirelessPen secure for everyone.**