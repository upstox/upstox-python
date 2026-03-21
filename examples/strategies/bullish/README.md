# Bullish Strategies

These scripts place bullish options trades on Nifty 50 using the Upstox Python SDK. Use them when you think the market is going to go **up**.

**Before running:** Replace `ACCESS_TOKEN` in each file with your Upstox access token.

> **Works on any index:** Change `"Nifty 50"` in `search_instrument()` to trade a different index — e.g. `"Nifty Bank"` for Bank Nifty or `"SENSEX"` for BSE Sensex.

---

## Buy Call — [code/buy_call.py](code/buy_call.py)

**When to use:** You strongly believe Nifty will go up in the next few days.

**What it does:** Buys one ATM call option. A call option gains value as the market rises. If the market falls instead, you only lose the premium you paid — nothing more.

Think of it like placing a bet: you pay a fixed amount upfront, and if the market moves in your favour, you profit. If it doesn't, your loss is capped at what you paid.

**Example:**
- Nifty is at 23,100. You buy the 23100 CE for ₹150.
- Nifty goes up to 23,400 by expiry → you make **₹150 profit** (300 points gain minus ₹150 premium)
- Nifty falls to 23,000 by expiry → option expires worthless, you lose **₹150** (your premium)

```
You profit when : Nifty closes above 23,250 (strike + premium)
Max profit      : Unlimited — grows as Nifty rises
Max loss        : ₹150 per unit — the premium you paid
```

**Run:**
```bash
python3 code/buy_call.py
```

---

## Sell Put — [code/sell_put.py](code/sell_put.py)

**When to use:** You think Nifty will stay flat or go slightly up — not necessarily a big rally.

**What it does:** Sells one ATM put option and collects premium upfront. As long as the market doesn't fall much, you keep the premium as profit. If the market falls sharply, losses can be significant.

Think of it like being an insurance seller — you collect a fee, and the trade is fine unless something goes badly wrong.

**Example:**
- Nifty is at 23,100. You sell the 23100 PE and collect ₹130.
- Nifty stays at 23,100 or goes up by expiry → put expires worthless, you keep **₹130**
- Nifty falls to 22,800 by expiry → you lose ₹300 but already collected ₹130, net loss = **₹170**

```
You profit when : Nifty closes above 22,970 (strike − premium)
Max profit      : ₹130 per unit — the premium you collected
Max loss        : Large if Nifty falls sharply below the strike
```

**Run:**
```bash
python3 code/sell_put.py
```

---

## Bull Call Spread — [code/bull_call_spread.py](code/bull_call_spread.py)

**When to use:** You expect Nifty to go up moderately — not a big move, but a steady rise. You want to reduce the cost compared to simply buying a call.

**What it does:** Buys an ATM call (lower strike) and sells an OTM call (one strike above). The premium received from the sold call reduces how much you pay. The trade-off: your profit is capped — you won't benefit if Nifty shoots up beyond the upper strike.

**Example:**
- Nifty is at 23,100. Buy 23100 CE for ₹150, Sell 23150 CE for ₹110. You pay a net ₹40.
- Nifty goes to 23,200 by expiry → max profit = **₹10 per unit** (50 point spread minus ₹40 cost)
- Nifty falls to 23,000 by expiry → both options expire worthless, you lose **₹40**

```
You profit when : Nifty closes above 23,140 (lower strike + net cost)
Max profit      : ₹10 per unit — if Nifty closes at or above 23,150
Max loss        : ₹40 per unit — the net premium you paid
```

> **Why use this over a plain Buy Call?** It's cheaper. You sacrifice some upside profit but pay less upfront.

**Run:**
```bash
python3 code/bull_call_spread.py
```

---

## Bull Put Spread — [code/bull_put_spread.py](code/bull_put_spread.py)

**When to use:** You expect Nifty to stay above a certain level. You want to earn premium without taking on large downside risk.

**What it does:** Sells an ATM put (collects premium) and buys a lower OTM put (pays a smaller premium as protection). The bought put limits how much you can lose if the market falls. You keep the difference — the net credit — as profit if the market stays above the sold strike.

**Example:**
- Nifty is at 23,100. Sell 23100 PE for ₹130, Buy 23050 PE for ₹95. Net credit = ₹35.
- Nifty stays above 23,100 at expiry → both puts expire worthless, you keep **₹35**
- Nifty falls to 22,900 at expiry → max loss = ₹50 (spread width) − ₹35 = **₹15 per unit**

```
You profit when : Nifty closes above 23,065 (short strike − net credit)
Max profit      : ₹35 per unit — the net premium collected
Max loss        : ₹15 per unit — capped by the bought put
```

> **Why use this over a plain Sell Put?** The bought put acts as a safety net — your loss is limited no matter how far the market falls.

**Run:**
```bash
python3 code/bull_put_spread.py
```
