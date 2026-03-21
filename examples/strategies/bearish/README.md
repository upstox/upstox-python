# Bearish Strategies

These scripts place bearish options trades on Nifty 50 using the Upstox Python SDK. Use them when you think the market is going to go **down**.

**Before running:** Replace `ACCESS_TOKEN` in each file with your Upstox access token.

> **Works on any index:** Change `"Nifty 50"` in `search_instrument()` to trade a different index — e.g. `"Nifty Bank"` for Bank Nifty or `"SENSEX"` for BSE Sensex.

---

## Buy Put — [code/buy_put.py](code/buy_put.py)

**When to use:** You strongly believe Nifty will fall in the next few days.

**What it does:** Buys one ATM put option. A put option gains value as the market falls. If the market rises instead, you only lose the premium you paid — nothing more.

Think of it like the mirror image of buying a call — same fixed-risk structure, but you profit from a fall instead of a rise.

**Example:**
- Nifty is at 23,100. You buy the 23100 PE for ₹130.
- Nifty falls to 22,800 by expiry → you make **₹170 profit** (300 points gain minus ₹130 premium)
- Nifty rises to 23,300 by expiry → option expires worthless, you lose **₹130** (your premium)

```
You profit when : Nifty closes below 22,970 (strike − premium)
Max profit      : Grows as Nifty falls further
Max loss        : ₹130 per unit — the premium you paid
```

**Run:**
```bash
python3 code/buy_put.py
```

---

## Sell Call — [code/sell_call.py](code/sell_call.py)

**When to use:** You think Nifty will stay flat or drift slightly lower — not necessarily a big crash.

**What it does:** Sells one ATM call option and collects premium upfront. As long as the market doesn't rise much, you keep the premium as profit. If the market rallies sharply, losses can be significant.

Think of it like the bearish version of selling a put — you collect a fee and hope nothing unexpected happens on the upside.

**Example:**
- Nifty is at 23,100. You sell the 23100 CE and collect ₹150.
- Nifty stays at 23,100 or goes down by expiry → call expires worthless, you keep **₹150**
- Nifty rises to 23,400 by expiry → you lose ₹300 but already collected ₹150, net loss = **₹150**

```
You profit when : Nifty closes below 23,250 (strike + premium)
Max profit      : ₹150 per unit — the premium you collected
Max loss        : Large if Nifty rallies sharply above the strike
```

**Run:**
```bash
python3 code/sell_call.py
```

---

## Bear Call Spread — [code/bear_call_spread.py](code/bear_call_spread.py)

**When to use:** You expect Nifty to stay flat or fall moderately. You want to earn premium but with a safety net on the upside.

**What it does:** Sells an ATM call (collects premium) and buys an OTM call one strike above (pays a smaller premium as protection). The bought call limits your loss if the market rises unexpectedly. You keep the net credit as profit if Nifty stays below the sold strike.

**Example:**
- Nifty is at 23,100. Sell 23100 CE for ₹150, Buy 23150 CE for ₹110. Net credit = ₹40.
- Nifty stays below 23,100 at expiry → both calls expire worthless, you keep **₹40**
- Nifty rises to 23,300 at expiry → max loss = ₹50 (spread width) − ₹40 = **₹10 per unit**

```
You profit when : Nifty closes below 23,140 (short strike + net credit)
Max profit      : ₹40 per unit — the net premium collected
Max loss        : ₹10 per unit — capped by the bought call
```

> **Why use this over a plain Sell Call?** The bought call acts as a safety net — your loss is capped no matter how far the market rises.

**Run:**
```bash
python3 code/bear_call_spread.py
```

---

## Bear Put Spread — [code/bear_put_spread.py](code/bear_put_spread.py)

**When to use:** You expect Nifty to fall moderately — not a huge crash, but a noticeable move down. You want cheaper entry than buying a put outright.

**What it does:** Buys an ATM put (higher strike) and sells a lower OTM put. The premium received from the sold put reduces the net cost. The trade-off: your profit is capped — you won't benefit if Nifty crashes far below the lower strike.

**Example:**
- Nifty is at 23,100. Buy 23100 PE for ₹130, Sell 23050 PE for ₹95. Net cost = ₹35.
- Nifty falls to 22,900 by expiry → max profit = **₹15 per unit** (50 point spread minus ₹35 cost)
- Nifty rises to 23,300 by expiry → both options expire worthless, you lose **₹35**

```
You profit when : Nifty closes below 23,065 (higher strike − net cost)
Max profit      : ₹15 per unit — if Nifty closes at or below 23,050
Max loss        : ₹35 per unit — the net premium you paid
```

> **Why use this over a plain Buy Put?** It's cheaper. You give up profits from a large crash but pay less upfront.

**Run:**
```bash
python3 code/bear_put_spread.py
```
