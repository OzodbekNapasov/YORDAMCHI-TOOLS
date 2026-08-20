import requests
try:
    from meta_ads_bot.config import META_ACCESS_TOKEN, AD_ACCOUNT_ID, META_GRAPH_URL
except ImportError:
    from config import META_ACCESS_TOKEN, AD_ACCOUNT_ID, META_GRAPH_URL

class MetaAdsManager:
    def __init__(self, token=None, account_id=None):
        self.token = token or META_ACCESS_TOKEN
        self.account_id = account_id or AD_ACCOUNT_ID
        self.base_url = META_GRAPH_URL

    def _get(self, endpoint, params=None):
        if params is None:
            params = {}
        params['access_token'] = self.token
        url = f"{self.base_url}/{endpoint}"
        try:
            resp = requests.get(url, params=params, timeout=15)
            data = resp.json()
            if "error" in data:
                print(f"[Meta API Error GET {endpoint}]:", data["error"])
            return data
        except Exception as e:
            print(f"[Meta API Exception GET {endpoint}]:", e)
            return {"error": {"message": str(e)}}

    def _post(self, endpoint, data=None):
        if data is None:
            data = {}
        data['access_token'] = self.token
        url = f"{self.base_url}/{endpoint}"
        try:
            resp = requests.post(url, data=data, timeout=15)
            res_data = resp.json()
            if "error" in res_data:
                print(f"[Meta API Error POST {endpoint}]:", res_data["error"])
            return res_data
        except Exception as e:
            print(f"[Meta API Exception POST {endpoint}]:", e)
            return {"error": {"message": str(e)}}

    def get_account_info(self):
        """Hisob ma'lumotlari, balans, xarajat va valyutani oladi"""
        fields = "name,account_status,amount_spent,balance,currency,spend_cap,min_daily_budget,disable_reason,funding_source_details,is_prepay_account"
        res = self._get(self.account_id, {"fields": fields})
        return res

    def get_balance_details(self, custom_budget_limit=None):
        """Hisob balansi, sarflangan va qolgan pulni hisoblaydi"""
        acc = self.get_account_info()
        if "error" in acc:
            return {"error": acc["error"]}

        currency = acc.get("currency", "USD")
        is_prepay = acc.get("is_prepay_account", False)
        
        # Meta amount_spent (har doim sentlarda keladi: 314 sent = 3.14 USD)
        raw_spent = float(acc.get("amount_spent", 0))
        amount_spent = raw_spent / 100.0
        
        # Meta balance (har doim sentlarda keladi)
        raw_balance = float(acc.get("balance", 0))
        current_balance = raw_balance / 100.0

        # Spend Cap
        raw_cap = float(acc.get("spend_cap", 0))
        spend_cap = raw_cap / 100.0 if raw_cap > 0 else 0

        # Karta ma'lumotlari
        card = acc.get("funding_source_details", {}).get("display_string", "Biriktirilgan karta")

        # Hisoblash:
        effective_limit = custom_budget_limit if (custom_budget_limit is not None and custom_budget_limit > 0) else spend_cap

        if effective_limit > 0:
            remaining = max(0.0, effective_limit - amount_spent)
        else:
            remaining = None

        return {
            "account_name": acc.get("name"),
            "account_status": acc.get("account_status"),
            "is_prepay": is_prepay,
            "currency": currency,
            "card": card,
            "amount_spent": amount_spent,
            "current_balance": current_balance,
            "spend_cap": spend_cap,
            "effective_limit": effective_limit,
            "remaining": remaining
        }

    def get_campaigns(self, limit=25):
        """Barcha kampaniyalarni oladi"""
        fields = "id,name,status,effective_status,daily_budget,lifetime_budget,objective,start_time,stop_time"
        res = self._get(f"{self.account_id}/campaigns", {
            "fields": fields,
            "limit": limit
        })
        return res.get("data", [])

    def get_campaign(self, campaign_id):
        """Alohida bitta kampaniya ma'lumoti"""
        fields = "id,name,status,effective_status,daily_budget,lifetime_budget,objective,start_time,stop_time"
        return self._get(campaign_id, {"fields": fields})

    def set_campaign_status(self, campaign_id, status):
        """Kampaniyani ACTIVE yoki PAUSED qiladi"""
        status = status.upper()
        if status not in ["ACTIVE", "PAUSED"]:
            return {"error": {"message": "Noto'g'ri status. Faqat ACTIVE yoki PAUSED mumkin."}}
        return self._post(campaign_id, {"status": status})

    def set_campaign_budget(self, campaign_id, daily_budget_dollars):
        """Kampaniya kunlik byudjetini o'zgartiradi (dollarda)"""
        cents = int(float(daily_budget_dollars) * 100)
        return self._post(campaign_id, {"daily_budget": cents})

    def get_insights(self, date_preset="today", campaign_id=None):
        """Statistika olish (today, yesterday, last_7d, this_month)"""
        target = campaign_id if campaign_id else self.account_id
        fields = "spend,impressions,clicks,cpc,cpm,ctr,actions,cost_per_action_type,date_start,date_stop"
        res = self._get(f"{target}/insights", {
            "fields": fields,
            "date_preset": date_preset
        })
        
        data = res.get("data", [])
        if not data:
            return {
                "spend": "0.00",
                "impressions": "0",
                "clicks": "0",
                "ctr": "0.00%",
                "cpc": "$0.00",
                "cpm": "$0.00",
                "leads": "0",
                "cpl": "—",
                "date_start": "",
                "date_stop": ""
            }

        row = data[0]
        spend = float(row.get("spend", 0))
        impressions = int(row.get("impressions", 0))
        clicks = int(row.get("clicks", 0))
        ctr = float(row.get("ctr", 0))
        cpc = float(row.get("cpc", 0))
        cpm = float(row.get("cpm", 0))

        # Lidlar sonini hisoblash
        leads = 0
        actions = row.get("actions", [])
        for act in actions:
            if act.get("action_type") in ["lead", "onsite_conversion.lead_grouped", "offsite_complete_registration_add_meta_leads"]:
                leads = max(leads, int(act.get("value", 0)))

        cpl = (spend / leads) if leads > 0 else 0.0

        return {
            "spend": f"{spend:.2f}",
            "impressions": f"{impressions:,}",
            "clicks": f"{clicks:,}",
            "ctr": f"{ctr:.2f}%",
            "cpc": f"${cpc:.3f}",
            "cpm": f"${cpm:.2f}",
            "leads": str(leads),
            "cpl": f"${cpl:.2f}" if leads > 0 else "—",
            "date_start": row.get("date_start", ""),
            "date_stop": row.get("date_stop", "")
        }
