# Neutral Strategies

These scripts place neutral options trades on Nifty 50 using the Upstox Python SDK. Use them when you think the market is going to **stay in a range** — not move up or down significantly.

**Before running:** Replace `ACCESS_TOKEN` in each file with your Upstox access token.

> **Works on any index:** Change `"Nifty 50"` in `search_instrument()` to trade a different index — e.g. `"Nifty Bank"` for Bank Nifty or `"SENSEX"` for BSE Sensex.

---

## Short Straddle — [code/short_straddle.py](code/short_straddle.py)

**When to use:** You expect Nifty to barely move from its current level — low volatility, sideways market.

**What it does:** Sells both an ATM call and an ATM put at the same strike. You collect premium from both sides. As long as the market stays close to that strike, both options lose value and you profit. If the market moves sharply in either direction, losses can be large.

Think of it as betting that "nothing big will happen." You earn money from time decay as long as the market stays calm.

**Example:**
- Nifty is at 23,100. Sell 23100 CE for ₹150, Sell 23100 PE for ₹130. Total collected = ₹280.
- Nifty closes at 23,100 at expiry → both options expire worthless, you keep **₹280**
- Nifty rises to 23,500 at expiry → call is exercised against you, net loss = 400 − 280 = **₹120**
- Nifty falls to 22,700 at expiry → put is exercised against you, net loss = 400 − 280 = **₹120**

```
You profit when : Nifty closes between 22,820 and 23,380
Max profit      : ₹280 per unit — if Nifty closes exactly at 23,100
Max loss        : Grows if Nifty moves far beyond either breakeven — no hard cap
```

> **Note:** This strategy has unlimited risk on both sides. Use it only when you are confident the market will stay range-bound, or consider Iron Butterfly for a safer version.

**Run:**
```bash
python3 code/short_straddle.py
```

---

## Short Strangle — [code/short_strangle.py](code/short_strangle.py)

**When to use:** Similar to the straddle, but you are okay giving the market a bit more room to move. You expect Nifty to stay within a wider range.

**What it does:** Sells an OTM call (one strike above ATM) and an OTM put (one strike below ATM). Since both options are out-of-the-money, less premium is collected compared to a straddle — but the market has more breathing room before the trade starts losing.

**Example:**
- Nifty is at 23,100. Sell 23150 CE for ₹110, Sell 23050 PE for ₹95. Total collected = ₹205.
- Nifty closes anywhere between 23,050 and 23,150 at expiry → both expire worthless, you keep **₹205**
- Nifty rises to 23,500 at expiry → net loss = (23500 − 23150) − 205 = **₹145**
- Nifty falls to 22,700 at expiry → net loss = (23050 − 22700) − 205 = **₹145**

```
You profit when : Nifty closes between 22,845 and 23,355
Max profit      : ₹205 per unit — if Nifty stays between the two sold strikes
Max loss        : Grows if Nifty moves far beyond either breakeven — no hard cap
```

> **Straddle vs Strangle:** Strangle gives more room for the market to move but earns less premium. Straddle earns more but needs the market to stay very close to ATM.

**Run:**
```bash
python3 code/short_strangle.py
```

---

## Iron Butterfly — [code/iron_butterfly.py](code/iron_butterfly.py)

**When to use:** You expect Nifty to stay near its current level, but you want your losses to be capped — unlike the straddle where losses are unlimited.

**What it does:** Sells an ATM call and an ATM put (just like a straddle) to collect premium, but also buys an OTM call and an OTM put further away as protection. The bought options limit how much you can lose if the market moves sharply. You collect less premium overall, but your risk is fully defined.

**Example:**
- Nifty is at 23,100.
- Sell 23100 CE (₹150) + Sell 23100 PE (₹130) = ₹280 collected
- Buy 23200 CE (₹60) + Buy 23000 PE (₹55) = ₹115 paid as protection
- Net premium in hand = ₹165. Protection kicks in 100 points away from ATM.
- Nifty closes at 23,100 at expiry → max profit = **₹165 per unit**
- Nifty moves to 23,200 or 23,000 at expiry → loss is fully capped at the wing boundary

```
You profit when : Nifty closes between 22,935 and 23,265
Max profit      : ₹165 per unit — if Nifty closes at 23,100
Max loss        : Capped — cannot lose more than (wing width − net credit)
```

> **Why use this over a Straddle?** The Iron Butterfly is safer — your loss is always limited. Great for beginners stepping into neutral strategies.

**Run:**
```bash
python3 code/iron_butterfly.py
```

---

## Batman — [code/batman.py](code/batman.py)

**When to use:** You expect Nifty to stay range-bound but want two profit zones instead of one — one above and one below the current price. All risk is defined.

**What it does:** Combines a call butterfly and a put butterfly around the ATM strike. A butterfly spread makes money when the market closes near the middle strike of that butterfly. By building one on the call side and one on the put side, you create two peaks of profit — one slightly above ATM and one slightly below. The profit and loss zone resembles the Batman logo, giving the strategy its name.

You pay a small net premium to enter. Your loss cannot exceed that premium, no matter what the market does.

**Legs breakdown:**
- Call butterfly: BUY ATM CE → SELL 2× ATM+1 CE → BUY ATM+2 CE
- Put butterfly: BUY ATM PE → SELL 2× ATM-1 PE → BUY ATM-2 PE

**Example:**
- Nifty is at 23,100. Strikes used: 23000 / 23050 / 23100 / 23150 / 23200.
- Call butterfly net cost ≈ ₹10. Put butterfly net cost ≈ ₹5. Total net cost ≈ ₹15.
- Nifty closes near 23,150 at expiry → call butterfly pays off, profit ≈ **₹35 per unit**
- Nifty closes near 23,050 at expiry → put butterfly pays off, profit ≈ **₹30 per unit**
- Nifty closes at 22,800 or 23,400 at expiry → all options expire at max loss, you lose **≈ ₹15** (your net cost)

```
Profit zones : Near ATM+1 (call butterfly peak) and ATM-1 (put butterfly peak)
Max profit   : Varies — roughly 2–4× the net cost, at each inner strike
Max loss     : Net premium paid ≈ ₹15 per unit — fully defined, cannot lose more
```

> **Why Batman?** It's a low-cost, defined-risk strategy with two profit opportunities. Good when you expect the market to be slightly volatile but within a band.

**Run:**
```bash
python3 code/batman.py
```
