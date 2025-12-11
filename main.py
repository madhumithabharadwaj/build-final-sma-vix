from AlgorithmImports import *
from custom_data_vix import VIXDaily

class BuildFinalSmaVix(QCAlgorithm):

    def Initialize(self):
        # ---- Required meta ----
        self.SetStartDate(2018, 1, 1)
        self.SetEndDate(2024, 1, 1)
        self.SetCash(100000)

        # ---- Universe / asset ----
        self.spy = self.AddEquity("SPY", Resolution.Daily).Symbol

        # ---- External data (custom CSV) ----
        # If the CSV is missing or unreadable, we’ll safely continue without the filter.
        self.USE_VIX_FILTER = False

        try:
            self.vix_symbol = self.AddData(VIXDaily, "VIX", Resolution.Daily).Symbol
            # Warm up to ensure we have an initial reading
            self.SetWarmUp(200, Resolution.Daily)
        except Exception as e:
            self.USE_VIX_FILTER = False
            self.Debug(f"[WARN] VIX external data disabled: {e}")

        # ---- Indicators ----
        self.fast = self.SMA(self.spy, 50, Resolution.Daily)
        self.slow = self.SMA(self.spy, 200, Resolution.Daily)

        # ---- Risk / failure-mode settings ----
        self.max_drawdown_pct = -0.05   # simple stop (−5% from entry)
        self.last_entry_price = None
        self.last_vix = None
        self.vix_threshold = 25.0       # only trade if VIX < 25 (calm regime)

        # Daily schedule to check conditions near market open
        self.Schedule.On(self.DateRules.EveryDay(self.spy),
                         self.TimeRules.AfterMarketOpen(self.spy, 10),
                         self.TradeLogic)

    def OnData(self, data: Slice):
        # Capture latest VIX value if present (external data failure-safe)
        if self.USE_VIX_FILTER and self.vix_symbol in data and data[self.vix_symbol] is not None:
            self.last_vix = float(data[self.vix_symbol].Value)

        # (No trading here; we do it in scheduled TradeLogic to avoid noisy intraday triggers)
        pass

    def TradeLogic(self):
        # 1) Make sure indicators are ready
        if self.IsWarmingUp or not (self.fast.IsReady and self.slow.IsReady):
            return

        # 2) Failure-mode handling for external data
        vix_ok = True
        if self.USE_VIX_FILTER:
            if self.last_vix is None:
                # If VIX hasn’t arrived yet today, treat as not OK (conservative)
                vix_ok = False
            else:
                vix_ok = self.last_vix < self.vix_threshold

        # 3) Simple trend rule
        trend_up = self.fast.Current.Value > self.slow.Current.Value

        invested = self.Portfolio[self.spy].Invested

        # 4) Risk guard: stop out if drawdown exceeds threshold
        if invested and self.last_entry_price is not None:
            pnl_pct = (self.Securities[self.spy].Price - self.last_entry_price) / self.last_entry_price
            if pnl_pct <= self.max_drawdown_pct:
                self.Debug(f"[STOP] Drawdown {pnl_pct:.2%} – Liquidating.")
                self.Liquidate(self.spy)
                self.last_entry_price = None
                return

        # 5) Entry / Exit
        if not invested and trend_up and vix_ok:
            qty = self.CalculateOrderQuantity(self.spy, 0.95)  # use ~95% to avoid margin errors
            if qty > 0:
                self.MarketOrder(self.spy, qty)
                self.last_entry_price = self.Securities[self.spy].Price
                self.Debug(f"[BUY] SPY @ {self.last_entry_price:.2f}; VIX={self.last_vix}")
        elif invested and (not trend_up or not vix_ok):
            self.Debug(f"[EXIT] trend_ok={trend_up} vix_ok={vix_ok} VIX={self.last_vix}")
            self.Liquidate(self.spy)
            self.last_entry_price = None

    # Defensive: if external data fails hard, keep running without it
    def OnSecuritiesChanged(self, changes):
        pass
