# Architecture Overview

Almora is structured around clean architecture principles to separate core domain logic, infrastructure components, models, and application interfaces.

---

## 🏛️ High-Level Design

```
+-------------------------------------------------------+
|                    Application Layer                  |
|                 (src/almora/app/)                     |
+-------------------------------------------------------+
                           |
                           v
+-------------------------------------------------------+
|                  Services & Domain                    |
|             (src/almora/services/)                    |
+-------------------------------------------------------+
       |                                   |
       v                                   v
+-----------------------+       +-----------------------+
|      Core & Models    |       |     Infrastructure    |
| (src/almora/core/)    |       | (infrastructure/)     |
| (src/almora/models/)  |       +-----------------------+
+-----------------------+
```

---

## 🔑 Key Principles

1. **Separation of Concerns**: Core domain rules do not depend on external UI or storage details.
2. **Predictable State Management**: Setting items use a staged two-step update pattern (`prepare` -> `apply`).
3. **Extensibility**: Specialized input controls extend base `SettingsItem` abstractions cleanly.
