#!/usr/bin/env python3
"""
Test runner for all Upstox API examples.

Runs every example against a real token and validates it. Success-path examples
must exit 0, print non-empty output, and raise no traceback. A separate
edge-case suite feeds deliberately-bad inputs and asserts the example fails
*gracefully* (non-zero exit via die(), no traceback).

Usage:
    python test_runner.py --token <TOKEN>
    python test_runner.py                 # prompts for the token interactively
"""

import argparse
import subprocess
import sys
import os
from datetime import date, timedelta


def _next_thursday() -> str:
    today = date.today()
    delta = (3 - today.weekday()) % 7
    if delta == 0:
        delta = 7
    return (today + timedelta(days=delta)).isoformat()


NEXT_THU = _next_thursday()
# A date guaranteed to parse; get_holiday returns a "not a holiday" result (exit 0)
# even when it isn't one, so any valid date exercises the endpoint.
SAMPLE_DATE = f"{date.today().year}-01-26"

def validate_token(token):
    """Make a lightweight API call to confirm the token works. Returns (ok, message)."""
    here = os.path.dirname(os.path.abspath(__file__))
    script = "\n".join([
        "import sys",
        "sys.path.insert(0, '.')",
        "from utils import get_api_client, search_instrument",
        f"client = get_api_client({token!r})",
        "resp = search_instrument(client, 'NIFTY', exchanges='NSE', segments='EQ', records=1)",
        "sys.exit(0 if resp and resp.data is not None else 1)",
    ])
    result = subprocess.run(
        [PYTHON, "-c", script],
        cwd=here,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode == 0:
        return True, "Token valid."
    stderr = result.stderr
    if "401" in stderr or "Unauthorized" in stderr or "UDAPI100068" in stderr:
        return False, "Token rejected (401 Unauthorized)."
    if "403" in stderr:
        return False, "Token rejected (403 Forbidden)."
    if stderr.strip():
        return False, stderr.strip().splitlines()[-1]
    return False, "Token validation failed."

def _find_python():
    """Use venv Python if one exists in the project root, else fall back to current interpreter."""
    here = os.path.dirname(os.path.abspath(__file__))
    for candidate in (
        os.path.join(here, "bin", "python3"),
        os.path.join(here, "bin", "python"),
        os.path.join(here, ".venv", "bin", "python3"),
        os.path.join(here, "venv", "bin", "python3"),
    ):
        if os.path.isfile(candidate):
            return candidate
    return sys.executable

PYTHON = _find_python()

# ── All examples in order ────────────────────────────────────────────────────

EXAMPLES = [
    # (category, script, extra_args)
    ("Instrument Search",   "instrument_search/search_equity.py",              ["--query", "RELIANCE"]),
    ("Instrument Search",   "instrument_search/search_futures.py",             ["--query", "NIFTY"]),
    ("Instrument Search",   "instrument_search/search_options.py",             ["--query", "NIFTY"]),

    ("Futures & Basis",     "futures_basis/nifty_futures_spread.py",           []),
    ("Futures & Basis",     "futures_basis/banknifty_futures_spread.py",       []),
    ("Futures & Basis",     "futures_basis/cash_futures_basis.py",             []),
    ("Futures & Basis",     "futures_basis/futures_roll_cost.py",              []),
    ("Futures & Basis",     "futures_basis/mcx_crude_spread.py",               []),

    ("Options Strategies",  "options_strategies/straddle_pricer.py",           ["--query", "NIFTY"]),
    ("Options Strategies",  "options_strategies/strangle_pricer.py",           ["--query", "NIFTY"]),
    ("Options Strategies",  "options_strategies/bull_call_spread.py",          ["--query", "NIFTY"]),
    ("Options Strategies",  "options_strategies/iron_condor_setup.py",         ["--query", "NIFTY"]),
    ("Options Strategies",  "options_strategies/butterfly_spread.py",          ["--query", "NIFTY"]),
    ("Options Strategies",  "options_strategies/calendar_spread_options.py",   ["--query", "NIFTY"]),
    ("Options Strategies",  "options_strategies/put_call_parity.py",           ["--query", "NIFTY"]),

    ("Options Analytics",   "options_analytics/options_chain_builder.py",      ["--query", "NIFTY", "--strikes", "3"]),
    ("Options Analytics",   "options_analytics/max_pain_calculator.py",        ["--query", "NIFTY"]),
    ("Options Analytics",   "options_analytics/oi_skew.py",                    ["--query", "NIFTY"]),
    ("Options Analytics",   "options_analytics/volatility_skew.py",            ["--query", "NIFTY"]),
    ("Options Analytics",   "options_analytics/gamma_exposure.py",             ["--query", "NIFTY"]),

    ("Arbitrage",           "arbitrage/nse_bse_arbitrage.py",                  ["--query", "RELIANCE"]),
    ("Arbitrage",           "arbitrage/etf_vs_index.py",                       []),
    ("Arbitrage",           "arbitrage/currency_futures_spread.py",            []),

    ("Historical Analysis", "historical_analysis/historical_candle.py",        ["--query", "RELIANCE"]),
    ("Historical Analysis", "historical_analysis/moving_average.py",           ["--query", "RELIANCE"]),
    ("Historical Analysis", "historical_analysis/historical_volatility.py",    ["--query", "RELIANCE"]),
    ("Historical Analysis", "historical_analysis/week_52_high_low.py",         ["--query", "RELIANCE"]),

    ("Portfolio Screening", "portfolio_screening/sector_index_comparison.py",  []),
    ("Portfolio Screening", "portfolio_screening/top_volume_stocks.py",        []),
    ("Portfolio Screening", "portfolio_screening/futures_oi_buildup.py",       []),

    ("Market Data",         "market_data/intraday_chart.py",                   ["--query", "SENSEX"]),
    ("Market Data",         "market_data/market_status.py",                    []),
    ("Market Data",         "market_data/market_holidays.py",                  []),
    ("Market Data",         "market_data/market_timings.py",                   []),
    ("Market Data",         "market_data/live_depth.py",                       []),      # streaming — auto-aborted after 5s
    ("Market Data",         "market_data/live_depth_d30.py",                   []),      # streaming — auto-aborted after 5s (Plus Pack)
    ("Market Data",         "market_data/live_depth_mcx.py",                   []),      # streaming — auto-aborted after 5s
    ("Market Data",         "market_data/live_depth_usdinr.py",                []),      # streaming — auto-aborted after 5s

    ("Options Analytics",   "options_analytics/option_chain_native.py",        ["--query", "NIFTY"]),
    ("Options Analytics",   "options_analytics/option_greeks.py",              ["--query", "NIFTY", "--strikes", "3"]),
    ("Options Analytics",   "options_analytics/pcr_trend.py",                  ["--query", "NIFTY"]),
    ("Options Analytics",   "options_analytics/iv_percentile.py",              ["--query", "NIFTY"]),
    ("Options Analytics",   "options_analytics/implied_move.py",               ["--query", "NIFTY"]),
    ("Options Analytics",   "options_analytics/expiry_decay.py",               ["--query", "NIFTY", "--strikes", "3"]),

    ("Historical Analysis", "historical_analysis/vwap.py",                     ["--query", "RELIANCE"]),
    ("Historical Analysis", "historical_analysis/beta_calculator.py",          ["--query", "RELIANCE"]),
    ("Historical Analysis", "historical_analysis/stock_correlation.py",        ["--queries", "RELIANCE,TCS,INFY"]),

    ("Fundamentals Analysis", "fundamentals/company_profile.py",               ["--symbol", "RELIANCE"]),
    ("Fundamentals Analysis", "fundamentals/key_ratios.py",                    ["--symbol", "RELIANCE"]),
    ("Fundamentals Analysis", "fundamentals/balance_sheet.py",                 ["--symbol", "RELIANCE"]),
    ("Fundamentals Analysis", "fundamentals/income_statement.py",              ["--symbol", "RELIANCE"]),
    ("Fundamentals Analysis", "fundamentals/cash_flow.py",                     ["--symbol", "RELIANCE"]),
    ("Fundamentals Analysis", "fundamentals/corporate_actions.py",             ["--symbol", "RELIANCE"]),
    ("Fundamentals Analysis", "fundamentals/share_holdings.py",                ["--symbol", "RELIANCE"]),
    ("Fundamentals Analysis", "fundamentals/competitors.py",                   ["--symbol", "RELIANCE"]),

    ("Market Information",  "market_information/fii_data.py",                  ["--data-type", "NSE_EQ|CASH", "--interval", "1D"]),
    ("Market Information",  "market_information/dii_data.py",                  ["--data-type", "NSE_EQ|CASH", "--interval", "1D"]),
    ("Market Information",  "market_information/oi_data.py",                   ["--expiry", NEXT_THU]),
    ("Market Information",  "market_information/change_oi.py",                 ["--expiry", NEXT_THU, "--interval", "5"]),
    ("Market Information",  "market_information/max_pain.py",                  ["--expiry", NEXT_THU, "--bucket-interval", "60"]),
    ("Market Information",  "market_information/pcr_data.py",                  ["--expiry", NEXT_THU, "--bucket-interval", "60"]),

    ("Account (Read-Only)", "account/user_profile.py",                         []),
    ("Account (Read-Only)", "account/funds_margin.py",                         []),

    ("Charges & Margin",    "charges/brokerage_calculator.py",                 ["--symbol", "RELIANCE"]),
    ("Charges & Margin",    "charges/margin_calculator.py",                    ["--symbol", "RELIANCE"]),

    ("Expired Instruments", "expired_instruments/expiries.py",                 ["--query", "NIFTY"]),
    ("Expired Instruments", "expired_instruments/expired_option_contracts.py", ["--query", "NIFTY"]),
    ("Expired Instruments", "expired_instruments/expired_future_contracts.py", ["--query", "NIFTY"]),
    ("Expired Instruments", "expired_instruments/expired_historical.py",       ["--query", "NIFTY"]),

    ("Market Data",         "market_data/ohlc_quote.py",                       ["--queries", "RELIANCE,TCS"]),
    ("Market Data",         "market_data/market_news.py",                      ["--query", "RELIANCE"]),
    ("Market Data",         "market_data/market_holiday.py",                   ["--date", SAMPLE_DATE]),

    ("Options Analytics",   "options_analytics/option_contracts.py",           ["--query", "NIFTY"]),
]

# Edge-case suite — deliberately-bad inputs. These MUST fail gracefully:
# non-zero exit via die() (message on stderr) and NO Python traceback.
EDGE_CASES = [
    # (category, script, extra_args)
    ("Edge Cases", "instrument_search/search_equity.py",     ["--query", "ZZZNOTAREALTICKER999"]),
    ("Edge Cases", "fundamentals/company_profile.py",        ["--symbol", "ZZZNOTAREALTICKER999"]),
    ("Edge Cases", "charges/brokerage_calculator.py",        ["--symbol", "ZZZNOTAREALTICKER999"]),
    ("Edge Cases", "market_information/oi_data.py",           ["--expiry", "not-a-real-date"]),
    ("Edge Cases", "market_data/market_holiday.py",           ["--date", "not-a-real-date"]),
]

# Scripts that run indefinitely — killed after this many seconds and counted as PASS
STREAMING_SCRIPTS = {
    "market_data/live_depth.py",
    "market_data/live_depth_d30.py",
    "market_data/live_depth_mcx.py",
    "market_data/live_depth_usdinr.py",
}
STREAMING_TIMEOUT = 5
DEFAULT_TIMEOUT = 90  # seconds for a non-streaming example before we call it hung

TRACEBACK_MARKER = "Traceback (most recent call last)"

# ── Helpers ───────────────────────────────────────────────────────────────────

BOLD  = "\033[1m"
GREEN = "\033[32m"
RED   = "\033[31m"
CYAN  = "\033[36m"
DIM   = "\033[2m"
RESET = "\033[0m"

def hr(char="─", width=70):
    print(char * width)

def _text(x):
    """Normalise captured stdout/stderr (str or bytes or None) to str."""
    if x is None:
        return ""
    return x.decode("utf-8", "replace") if isinstance(x, bytes) else x

def _echo(stdout, stderr):
    """Print the example's captured output so the run stays visible."""
    out = _text(stdout)
    if out.strip():
        print(out.rstrip())
    err = _text(stderr)
    if err.strip():
        print(f"{DIM}{err.rstrip()}{RESET}")

def run_example(script, token, extra_args, expect="success"):
    """
    Run one example and validate it. Returns (passed: bool, reason: str).

    expect="success"       — pass iff exit 0, non-empty stdout, no traceback.
    expect="graceful_fail" — pass iff non-zero exit and no traceback (die()'d).
    Streaming scripts pass when they run to the timeout window.
    """
    cmd = [PYTHON, script, "--token", token] + extra_args
    is_streaming = script in STREAMING_SCRIPTS
    timeout = STREAMING_TIMEOUT if is_streaming else DEFAULT_TIMEOUT
    try:
        result = subprocess.run(
            cmd, cwd=os.path.dirname(__file__),
            capture_output=True, text=True, timeout=timeout,
        )
        stdout, stderr, rc = result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired as e:
        _echo(e.stdout, e.stderr)
        if is_streaming:
            print(f"\n{DIM}  (streaming script auto-stopped after {STREAMING_TIMEOUT}s){RESET}")
            return True, "streaming ok"
        return False, f"timed out after {timeout}s"

    _echo(stdout, stderr)
    combined = _text(stdout) + _text(stderr)
    if TRACEBACK_MARKER in combined:
        return False, "uncaught exception (traceback)"

    if expect == "graceful_fail":
        if rc == 0:
            return False, "expected graceful failure but exited 0"
        return True, "failed gracefully"

    if rc != 0:
        return False, f"exit code {rc}"
    if not _text(stdout).strip():
        return False, "no output produced"
    return True, "ok"

# ── Main ──────────────────────────────────────────────────────────────────────

def _resolve_token(cli_token):
    """Use --token when supplied, else prompt interactively."""
    if cli_token:
        return cli_token.strip()
    try:
        return input("  Paste your Upstox analytics or access token: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nAborted.")
        sys.exit(0)


def run_suite(title, entries, token, expect, passed, failed, total, offset):
    """Run one group of examples, appending to passed/failed. Returns next offset."""
    current_category = None
    for j, (category, script, extra_args) in enumerate(entries):
        i = offset + j + 1
        if category != current_category:
            current_category = category
            print()
            print(f"{CYAN}{BOLD}  ── {category} {'─' * (50 - len(category))}{RESET}")

        print()
        print(f"{BOLD}  [{i}/{total}] {script}{RESET}")
        if extra_args:
            print(f"{DIM}  args: {' '.join(extra_args)}{RESET}")
        hr()

        ok, reason = run_example(script, token, extra_args, expect=expect)
        if ok:
            print(f"\n{GREEN}  ✓ PASSED{RESET} {DIM}({reason}){RESET}")
            passed.append(script)
        else:
            print(f"\n{RED}  ✗ FAILED — {reason}{RESET}")
            failed.append(f"{script}  [{reason}]")
    return offset + len(entries)


def main():
    parser = argparse.ArgumentParser(description="Run and validate all Upstox API examples")
    parser.add_argument("--token", default=None, help="Upstox access or analytics token")
    args = parser.parse_args()

    total = len(EXAMPLES) + len(EDGE_CASES)

    hr("═")
    print(f"{BOLD}  Upstox API Examples — Test Runner{RESET}")
    print(f"  {len(EXAMPLES)} examples + {len(EDGE_CASES)} edge cases = {total} checks")
    hr("═")
    print()

    token = _resolve_token(args.token)
    if not token:
        print(f"{RED}  No token provided. Exiting.{RESET}")
        sys.exit(1)

    print(f"  Validating token...", end=" ", flush=True)
    ok, msg = validate_token(token)
    if ok:
        print(f"{GREEN}✓ {msg}{RESET}")
    else:
        print(f"{RED}✗ {msg}{RESET}")
        sys.exit(1)

    passed = []
    failed = []

    offset = run_suite("Examples", EXAMPLES, token, "success", passed, failed, total, 0)
    run_suite("Edge Cases", EDGE_CASES, token, "graceful_fail", passed, failed, total, offset)

    # Summary
    print()
    hr("═")
    print(f"{BOLD}  Results: {GREEN}{len(passed)} passed{RESET}  {RED}{len(failed)} failed{RESET}  out of {len(passed)+len(failed)} run")
    hr("═")

    if failed:
        print(f"\n{RED}  Failed checks:{RESET}")
        for s in failed:
            print(f"    • {s}")
        print()
        sys.exit(1)

if __name__ == "__main__":
    main()
