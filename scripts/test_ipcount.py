from ipcount import aggregate_ips


def test_counts_basic():
    lines = [
        "[29/Sep/2021:10:29:16+0100] 10.32.89.34 /home DELETE curl/7.68.0",
        "[29/Sep/2021:10:21:46+0100] 10.32.89.34 /login PUT curl/7.68.0",
        "[29/Sep/2021:10:17:51+0100] 10.0.0.1 /login POST Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "[29/Sep/2021:10:50:10+0100] 172.32.9.12 /api/data GET PostmanRuntime/7.28.0",
        "[29/Sep/2021:10:38:27+0100] 10.0.0.1 /home GET Mozilla/5.0 (X11; Linux x86_64)",
        "[29/Sep/2021:10:06:42+0100] 192.168.22.11 /checkout DELETE Mozilla/5.0 (X11; Linux x86_64)",
        "[29/Sep/2021:10:03:46+0100] 10.32.89.34 /home DELETE curl/7.68.0",
        "[29/Sep/2021:10:49:18+0100] 172.16.0.5 /products DELETE PostmanRuntime/7.28.0",
        "[29/Sep/2021:10:04:27+0100] 121.89.25.43 /products DELETE curl/7.68.0",
        "[29/Sep/2021:10:24:26+0100] 10.32.89.34 /healthz GET curl/7.68.0",
    ]
    result = aggregate_ips(lines)
    assert result["10.32.89.34"] == 4
    assert result["10.0.0.1"] == 2
    assert set(result.keys()) == {"10.32.89.34", "10.0.0.1", "172.32.9.12", "192.168.22.11", "172.16.0.5", "121.89.25.43"}
