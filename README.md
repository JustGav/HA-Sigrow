# HA-Sigrow

Home Assistant integration for Sigrow remote environmental sensors.

![Sigrow Logo](custom_components/sigrow/icons/sigrow_logo.jpg)

## ✅ Features

- Auto-discovers **Sigrow remote units**
- Supports sensors like temperature, humidity, CO2, light, and more
- Fetches data via `/remote/{remote_id}/data`
- Automatically converts **temperature to °C**
- Only requires an **API key** via config flow

## 🔧 Installation

1. 📦 Add this repo to HACS as a **custom repository** (type: Integration)
2. 🛠 Restart Home Assistant
3. ➕ Go to **Settings > Devices & Services > Add Integration**
4. 🔑 Select **Sigrow** and enter your API key

## 🧪 Supported Devices

Only **remote units** are supported. Gateways or other devices will be ignored.

## 🛠 API Reference

Uses:
- [`GET /remote`](https://app.sigrow.com/api/v2/remote)
- [`GET /remote/{remote_id}/data`](https://app.sigrow.com/api/v2/remote/{remote_id}/data)

## 🧩 Credits

Created by [@JustGav](https://github.com/JustGav)  
Logo is a placeholder and can be updated for branding.

---

For questions, open an issue or contribute via pull request!
