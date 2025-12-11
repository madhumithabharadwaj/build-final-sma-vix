from AlgorithmImports import *

class VIXDaily(PythonData):
    """
    Minimal custom-data reader for a local CSV:
    CSV path: data/vix_daily.csv
    Format (header required):
        date,value
        2018-01-02,9.77
        2018-01-03,9.15
        ...
    """
    def GetSource(self, config, date, isLiveMode):
        # Reads a local project file (upload vix_daily.csv into /data)
        return SubscriptionDataSource("data/vix_daily.csv",
                                      SubscriptionTransportMedium.LocalFile,
                                      FileFormat.Csv)

    def Reader(self, config, line, date, isLiveMode):
        if not line or line.startswith("date"):
            return None
        try:
            parts = line.strip().split(",")
            v = VIXDaily()
            v.Symbol = config.Symbol
            v.Time = datetime.strptime(parts[0], "%Y-%m-%d")
            v.Value = float(parts[1])
            v["VIX"] = v.Value
            return v
        except Exception:
            # Graceful failure: skip bad lines so the algorithm keeps running
            return None
