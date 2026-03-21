# Other Strategies

These scripts implement options strategies that don't fit neatly into a single bullish, bearish, or neutral category. They combine directional and volatility views, or are primarily volatility plays regardless of market direction.

**Before running:** Replace `ACCESS_TOKEN` in each file with your Upstox access token.

> **Works on any index:** Change `"Nifty 50"` in `search_instrument()` to trade a different index — e.g. `"Nifty Bank"` for Bank Nifty or `"SENSEX"` for BSE Sensex.

---

## Call Ratio Spread — [code/call_ratio_spread.py](code/call_ratio_spread.py)

**When to use:** You expect a moderate upward move in Nifty but not a big rally. You want to enter at very low cost or even collect a small credit.

**What it does:** Buys one ATM call and sells two OTM calls (ATM+1). The two sold calls bring in more premium than the one bought call costs, so this trade is often entered at zero cost or a small net credit. Maximum profit is at the short strike (ATM+1). If Nifty rises sharply beyond ATM+1, the uncovered short call starts losing — this is the key risk.

**Example:**
- Nifty is at 23,100. Buy 23100 CE (₹150), Sell 2× 23150 CE (₹110 each). Net credit = ₹70.
- Nifty closes at 23,150 at expiry → long call gains ₹50, short calls expire worthless, profit = 50 + 70 = **₹120 per unit**
- Nifty closes at 23,000 at expiry → all calls expire worthless, profit = **₹70** (net credit kept)
- Nifty rises to 23,400 at expiry → long call gains ₹300, short calls lose 2×250 = ₹500, net = −200 + 70 = **₹130 loss**

```
You profit when : Nifty closes below 23,290 (approx upper breakeven)
Max profit      : ₹120 per unit — if Nifty closes exactly at 23,150
Max loss        : Increases as Nifty rises sharply above the short strike — no hard cap
```

> **Warning:** The uncovered portion of the short call creates unlimited upside risk. Always have a stop-loss in place if Nifty rallies strongly.

**Run:**
```bash
python3 code/call_ratio_spread.py
```

---

## Put Ratio Spread — [code/put_ratio_spread.py](code/put_ratio_spread.py)

**When to use:** You expect a moderate fall in Nifty but not a sharp crash. You want to enter at very low cost or collect a small credit.

**What it does:** Buys one ATM put and sells two OTM puts (ATM-1). The two sold puts generate more premium than the one bought put costs, so this trade is often entered at zero cost or a small net credit. Maximum profit is at the short strike (ATM-1). If Nifty falls sharply below ATM-1, the uncovered short put starts losing — this is the key risk.

**Example:**
- Nifty is at 23,100. Buy 23100 PE (₹130), Sell 2× 23050 PE (₹95 each). Net credit = ₹60.
- Nifty closes at 23,050 at expiry → long put gains ₹50, short puts expire worthless, profit = 50 + 60 = **₹110 per unit**
- Nifty stays at 23,200 at expiry → all puts expire worthless, profit = **₹60** (net credit kept)
- Nifty falls to 22,800 at expiry → long put gains ₹300, short puts lose 2×250 = ₹500, net = −200 + 60 = **₹140 loss**

```
You profit when : Nifty closes above 22,810 (approx lower breakeven)
Max profit      : ₹110 per unit — if Nifty closes exactly at 23,050
Max loss        : Increases as Nifty falls sharply below the short strike — no hard cap
```

> **Warning:** The uncovered portion of the short put creates large downside risk. Always have a stop-loss in place if Nifty falls sharply.

**Run:**
```bash
python3 code/put_ratio_spread.py
```

---

## Long Straddle — [code/long_straddle.py](code/long_straddle.py)

**When to use:** You expect a big move in Nifty but are unsure of the direction — for example, before a major event like RBI policy, budget, or election results.

**What it does:** Buys both an ATM call and an ATM put at the same strike. You profit if Nifty moves significantly in either direction — up or down. The total premium paid is your maximum loss, which occurs only if Nifty closes exactly at the strike at expiry. This is the opposite of the short straddle.

Think of it as paying for volatility. You don't care which way the market goes — you just need it to move enough to cover both premiums.

**Example:**
- Nifty is at 23,100. Buy 23100 CE for ₹150, Buy 23100 PE for ₹130. Total cost = ₹280.
- Nifty rises to 23,500 at expiry → call gains ₹400, put expires worthless, profit = 400 − 280 = **₹120 per unit**
- Nifty falls to 22,700 at expiry → put gains ₹400, call expires worthless, profit = 400 − 280 = **₹120 per unit**
- Nifty closes at 23,100 at expiry → both expire worthless, loss = **₹280 per unit**

```
Upper breakeven : 23,100 + 280 = 23,380
Lower breakeven : 23,100 − 280 = 22,820
Max profit      : Unlimited — grows as Nifty moves far in either direction
Max loss        : ₹280 per unit — if Nifty closes exactly at ATM strike
```

> **Long vs Short Straddle:** Long straddle profits from big moves; short straddle profits from calm markets. Choose based on your volatility expectation, not just direction.

**Run:**
```bash
python3 code/long_straddle.py
```

---

## Long Strangle — [code/long_strangle.py](code/long_strangle.py)

**When to use:** Same as the long straddle — you expect a big move but don't know the direction. You want a cheaper entry than the straddle and are okay with a wider breakeven range.

**What it does:** Buys an OTM call (ATM+1) and an OTM put (ATM-1). Since both options are already out of the money, they cost less than ATM options. Total premium paid is lower, but Nifty needs to move further before the trade starts making money.

**Example:**
- Nifty is at 23,100. Buy 23150 CE for ₹110, Buy 23050 PE for ₹95. Total cost = ₹205.
- Nifty rises to 23,500 at expiry → call gains ₹350, put expires worthless, profit = 350 − 205 = **₹145 per unit**
- Nifty falls to 22,700 at expiry → put gains ₹350, call expires worthless, profit = 350 − 205 = **₹145 per unit**
- Nifty closes anywhere between 23,050 and 23,150 at expiry → both expire worthless, loss = **₹205 per unit**

```
Upper breakeven : 23,150 + 205 = 23,355
Lower breakeven : 23,050 − 205 = 22,845
Max profit      : Grows as Nifty moves far in either direction
Max loss        : ₹205 per unit — if Nifty closes between the two bought strikes
```

> **Straddle vs Strangle:** Strangle is cheaper but needs a larger move to profit. Straddle costs more but starts profiting sooner. Pick strangle when you expect a large move; straddle when you expect a moderate but decisive move.

**Run:**
```bash
python3 code/long_strangle.py
```

---

## Long Iron Butterfly — [code/long_iron_butterfly.py](code/long_iron_butterfly.py)

**When to use:** You expect Nifty to move significantly away from its current level but want your risk and cost to be fully capped. The opposite of the iron butterfly.

**What it does:** Buys both an ATM call and ATM put (like a straddle), and sells an OTM call (ATM+2) and OTM put (ATM-2) as wings to reduce the net cost. The sold wings cap your maximum profit but significantly lower what you pay to enter. You profit if Nifty moves beyond the ATM strike by more than the net debit paid.

**Example:**
- Nifty is at 23,100.
- Buy 23100 CE (₹150) + Buy 23100 PE (₹130) = ₹280 paid
- Sell 23200 CE (₹60) + Sell 23000 PE (₹55) = ₹115 collected from wings
- Net cost = ₹165. Wing width = 100 points.
- Nifty rises to 23,300 at expiry → call spread gains 100, put expires worthless, profit = 100 − 165 = **−₹65** (still a loss within wing)
- Nifty rises beyond 23,200 → max profit = wing width − net debit = 100 − 165 → capped, profit zone kicks in above breakeven
- Nifty closes at 23,100 → both ATM options expire worthless, loss = **₹165 per unit** (max loss)

```
Upper breakeven : ATM strike + Net debit = 23,100 + 165 = 23,265
Lower breakeven : ATM strike − Net debit = 23,100 − 165 = 22,935
Max profit      : Wing width − Net debit — capped at the outer wings
Max loss        : ₹165 per unit — if Nifty closes exactly at ATM strike
```

> **Long Iron Butterfly vs Long Straddle:** The iron butterfly is cheaper to enter because the sold wings offset cost, but your profit is capped. Use it when you want defined risk on both cost and reward.

**Run:**
```bash
python3 code/long_iron_butterfly.py
```

---

## Long Iron Condor — [code/long_iron_condor.py](code/long_iron_condor.py)

**When to use:** You expect Nifty to break out of its current range but want fully capped risk. The opposite of the short iron condor.

**What it does:** Buys an OTM call (ATM+1) and an OTM put (ATM-1), and sells further OTM call (ATM+2) and put (ATM-2) wings to cap the cost. You pay a net debit. The trade profits if Nifty moves beyond either of the inner bought strikes by enough to cover the net debit paid. Both max profit and max loss are fully defined.

**Example:**
- Nifty is at 23,100.
- Buy 23150 CE (₹110) + Buy 23050 PE (₹95) = ₹205 paid
- Sell 23200 CE (₹60) + Sell 23000 PE (₹55) = ₹115 collected from wings
- Net cost = ₹90. Wing width = 50 points on each side.
- Nifty rises to 23,300 at expiry → call spread fully in profit = ₹50, profit = 50 − 90 = **−₹40** (within wing, still a loss)
- Nifty rises beyond 23,200 → max profit = wing width − net debit = 50 − 90 → capped
- Nifty closes between 22,960 and 23,240 → both spreads expire worthless or partially, loss up to **₹90**

```
Upper breakeven : Short call strike + Net debit = 23,150 + 90 = 23,240
Lower breakeven : Short put strike − Net debit  = 23,050 − 90 = 22,960
Max profit      : Wing width − Net debit — earned when Nifty moves beyond outer wings
Max loss        : ₹90 per unit — the net premium paid
```

> **Long Iron Condor vs Long Strangle:** Both profit from big moves, but the condor is cheaper because the wings cap your cost. The trade-off is capped profit. Use the condor when you want a cheaper, defined-risk volatility play.

**Run:**
```bash
python3 code/long_iron_condor.py
```

---

## Strip — [code/strip.py](code/strip.py)

**When to use:** You expect a big move in Nifty but lean towards a fall being more likely. You want to profit in either direction but earn more if the market drops.

**What it does:** Buys one ATM call and two ATM puts at the same strike. It's like a long straddle but with an extra put — so the downside pays out twice as much as the upside. You pay more premium than a straddle, but the additional put doubles your profit for every point Nifty falls below the breakeven. If Nifty rallies instead, you still profit, just at a slower rate.

Think of it as a straddle with a bearish tilt — you're not sure which way it goes, but you're guessing down is more likely.

**Example:**
- Nifty is at 23,100. Buy 23100 CE (₹150) + Buy 2× 23100 PE (₹130 each). Total cost = ₹410.
- Nifty falls to 22,700 at expiry → call worthless, 2 puts gain 2×400 = ₹800, profit = 800 − 410 = **₹390 per unit**
- Nifty rises to 23,600 at expiry → puts worthless, call gains ₹500, profit = 500 − 410 = **₹90 per unit**
- Nifty closes at 23,100 at expiry → all options expire worthless, loss = **₹410 per unit**

```
Upper breakeven : Strike + Total premium = 23,100 + 410 = 23,510
Lower breakeven : Strike − (Total premium ÷ 2) = 23,100 − 205 = 22,895
Max profit      : Unlimited on both sides — larger on the downside (2× puts)
Max loss        : ₹410 per unit — if Nifty closes exactly at the ATM strike
```

> **Strip vs Long Straddle:** Strip profits more on a big fall, less on a big rise. Use it when you expect volatility but have a slight bearish bias.

**Run:**
```bash
python3 code/strip.py
```

---

## Strap — [code/strap.py](code/strap.py)

**When to use:** You expect a big move in Nifty but lean towards a rise being more likely. You want to profit in either direction but earn more if the market rallies.

**What it does:** Buys two ATM calls and one ATM put at the same strike. It's like a long straddle but with an extra call — so the upside pays out twice as much as the downside. You pay more premium than a straddle, but the additional call doubles your profit for every point Nifty rises above the breakeven. If Nifty falls instead, you still profit, just at a slower rate.

Think of it as a straddle with a bullish tilt — you're not sure which way it goes, but you're guessing up is more likely.

**Example:**
- Nifty is at 23,100. Buy 2× 23100 CE (₹150 each) + Buy 23100 PE (₹130). Total cost = ₹430.
- Nifty rises to 23,600 at expiry → put worthless, 2 calls gain 2×500 = ₹1000, profit = 1000 − 430 = **₹570 per unit**
- Nifty falls to 22,700 at expiry → calls worthless, put gains ₹400, profit = 400 − 430 = **−₹30** (small loss — needs a bigger fall)
- Nifty falls to 22,670 at expiry → put gains ₹430, profit = **₹0** (lower breakeven)
- Nifty closes at 23,100 at expiry → all options expire worthless, loss = **₹430 per unit**

```
Upper breakeven : Strike + (Total premium ÷ 2) = 23,100 + 215 = 23,315
Lower breakeven : Strike − Total premium = 23,100 − 430 = 22,670
Max profit      : Unlimited on both sides — larger on the upside (2× calls)
Max loss        : ₹430 per unit — if Nifty closes exactly at the ATM strike
```

> **Strap vs Long Straddle:** Strap profits more on a big rally, less on a big fall. Use it when you expect volatility but have a slight bullish bias.

**Run:**
```bash
python3 code/strap.py
```
