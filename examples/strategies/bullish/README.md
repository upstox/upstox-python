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

---

## Bull Butterfly — [code/bull_butterfly.py](code/bull_butterfly.py)

**When to use:** You expect Nifty to rise to a specific level by expiry — not too much, not too little. You want a low-cost trade with a sharp profit peak right at your target price.

**What it does:** Uses three call strikes — buy one ATM call, sell two ATM+1 calls, and buy one ATM+2 call. The two sold calls bring in premium that makes this cheaper than a plain bull call spread. The sweet spot is Nifty closing exactly at ATM+1 (the middle strike) at expiry. If Nifty goes too far above or falls below, both max profit and max loss are fully capped.

Think of it as a sniper trade — low cost, defined risk, but you need Nifty to land close to your target strike to get the best payout.

**Example:**
- Nifty is at 23,100. Buy 23100 CE (₹150), Sell 2× 23150 CE (₹110 each), Buy 23200 CE (₹75).
- Net cost = (150 + 75) − (110 × 2) = **₹5 per unit**
- Nifty closes at 23,150 at expiry → max profit = spread width − net cost = 50 − 5 = **₹45 per unit**
- Nifty closes at 23,100 or below → all calls expire worthless, you lose **₹5**
- Nifty closes at 23,200 or above → gains and losses cancel out, you lose **₹5**

```
You profit when : Nifty closes between 23,105 and 23,195 (approx)
Max profit      : ₹45 per unit — if Nifty closes exactly at 23,150 (ATM+1)
Max loss        : ₹5 per unit — the small net premium you paid
```

> **Why use this over a Bull Call Spread?** Much cheaper entry. The trade-off is that your profit is concentrated at one specific price — the middle strike.

**Run:**
```bash
python3 code/bull_butterfly.py
```

---

## Bull Condor — [code/bull_condor.py](code/bull_condor.py)

**When to use:** You expect Nifty to rise moderately into a specific range — not too little, not too much. You want defined risk at a lower cost than a simple call spread.

**What it does:** Uses four call strikes in order — buy ATM, sell ATM+1, sell ATM+2, buy ATM+3. The two short calls in the middle bring in premium that reduces your net cost. Maximum profit is earned when Nifty closes anywhere between the two short strikes (ATM+1 and ATM+2) at expiry. Both max profit and max loss are fully capped.

Think of it as a bull call spread with an extra layer — you give up some profit potential to make the trade cheaper to enter.

**Example:**
- Nifty is at 23,100. Buy 23100 CE (₹150), Sell 23150 CE (₹110), Sell 23200 CE (₹75), Buy 23250 CE (₹45).
- Net cost = (150 + 45) − (110 + 75) = **₹10 per unit**
- Nifty closes between 23,150 and 23,200 at expiry → max profit = spread width − net cost = 50 − 10 = **₹40 per unit**
- Nifty closes at 23,100 or below → all calls expire worthless, you lose **₹10**
- Nifty closes at 23,250 or above → all spreads cancel out, you lose **₹10**

```
You profit when : Nifty closes between 23,110 and 23,240 (approx)
Max profit      : ₹40 per unit — if Nifty closes between 23,150 and 23,200
Max loss        : ₹10 per unit — the net premium you paid
```

> **Why use this over a Bull Call Spread?** Lower upfront cost. You cap your upside further but pay significantly less to enter the trade.

**Run:**
```bash
python3 code/bull_condor.py
```

---

## Long Calendar with Calls — [code/long_calendar_call.py](code/long_calendar_call.py)

**When to use:** You expect Nifty to stay near its current level in the short term but move up over the coming week. You want to use time decay to your advantage.

**What it does:** Sells a current-week ATM call and buys a next-week ATM call at the same strike. The near-term call loses value faster (time decay is quicker closer to expiry), so you profit from that decay while still holding a longer-dated call that benefits if Nifty rises after the near-term expiry.

Think of it as a two-phase trade — first earn from the near-term option expiring, then ride any upside through the longer-dated call you still own.

**Example:**
- Nifty is at 23,100. Sell current-week 23100 CE for ₹80, Buy next-week 23100 CE for ₹150. Net cost = ₹70.
- Nifty stays near 23,100 through current-week expiry → near-term call expires worthless, you keep ₹80. You still own the next-week call worth ₹150 (or more if Nifty rises).
- Nifty rises to 23,400 after current-week expiry → next-week call gains value significantly, overall profit grows.
- Nifty falls sharply → both calls lose value, max loss is the ₹70 net cost you paid.

```
You profit when : Nifty stays near ATM through near-term expiry, then rises
Max profit      : Varies — depends on how much the far-term call gains after near-term expires
Max loss        : ₹70 per unit — the net premium you paid (difference between the two calls)
```

> **Key difference from other strategies:** This trade spans two expiries. You are not just betting on direction — you are also betting on *when* the move happens.

**Run:**
```bash
python3 code/long_calendar_call.py
```

---

## Long Synthetic Future — [code/long_synthetic_future.py](code/long_synthetic_future.py)

**When to use:** You have a strong bullish view and want the same profit/loss profile as buying a futures contract, but using options instead.

**What it does:** Buys an ATM call and sells an ATM put at the same strike and expiry. The premium collected from the sold put largely offsets the cost of the bought call, making this a near-zero-cost position. From this point, the trade behaves exactly like a long futures position — you profit point-for-point as Nifty rises, and lose point-for-point as it falls.

Think of it as a futures position built from options. You get the same unlimited upside and unlimited downside, but with the flexibility of options (no daily MTM settlement like futures).

**Example:**
- Nifty is at 23,100. Buy 23100 CE for ₹150, Sell 23100 PE for ₹130. Net cost = ₹20.
- Nifty rises to 23,500 at expiry → call pays ₹400, put expires worthless, profit = 400 − 20 = **₹380 per unit**
- Nifty falls to 22,700 at expiry → call expires worthless, put is exercised against you, loss = 400 + 20 = **₹420 per unit**
- Nifty closes exactly at 23,100 → both expire worthless, you lose only **₹20** (net cost paid)

```
You profit when : Nifty closes above 23,120 (strike + net cost)
Max profit      : Unlimited — grows point-for-point as Nifty rises
Max loss        : Unlimited — grows point-for-point as Nifty falls
```

> **How is this different from just buying a futures contract?** The payoff is identical, but you avoid daily mark-to-market settlements. However, the risk is just as large — do not use this strategy without a clear stop-loss plan.

**Run:**
```bash
python3 code/long_synthetic_future.py
```

---

## Call Ratio Back Spread — [code/call_ratio_back_spread.py](code/call_ratio_back_spread.py)

**When to use:** You expect a sharp, significant rally in Nifty. You want to benefit from a big upside move while keeping entry cost low — ideally entering for free or a small credit.

**What it does:** Sells one ATM call and uses that premium to buy two OTM calls (ATM+1). The sold ATM call finances most or all of the cost of the two bought calls. The trade has a zone of maximum loss around the short strike but profits substantially if Nifty rallies sharply above the long call strikes. If Nifty stays flat or falls, you keep the small net credit (if any).

Think of it as paying for a big upside move with the premium collected from selling a closer call. The more Nifty rises, the more you profit — because you hold two long calls.

**Example:**
- Nifty is at 23,100. Sell 23100 CE (₹150), Buy 2× 23150 CE (₹110 each). Net credit = ₹150 − ₹220 = **−₹70 net debit**.
- Nifty closes at 23,150 at expiry → short call loses ₹50, long calls expire worthless, loss = 50 + 70 = **₹120** (max loss zone)
- Nifty rises to 23,400 at expiry → short call loses ₹300, 2 long calls gain 2×250 = ₹500, net = 500 − 300 − 70 = **₹130 profit**
- Nifty stays below 23,100 at expiry → all calls expire worthless, loss = **₹70** (net debit paid)

```
You profit when : Nifty rallies significantly above ATM+1 strike
Max profit      : Grows as Nifty rises sharply — 2 long calls accelerate gains
Max loss        : At the long call strike (ATM+1) — limited, predictable zone
```

> **Call Ratio Back Spread vs Buy Call:** Back spread profits much more on a large rally due to 2× long calls, at a lower entry cost. The trade-off is a loss zone near the short strike if Nifty rises only slightly.

**Run:**
```bash
python3 code/call_ratio_back_spread.py
```

---

## Range Forward — [code/range_forward.py](code/range_forward.py)

**When to use:** You have a clear bullish view and want upside exposure at very low cost — or even for free — by funding the call with a sold put.

**What it does:** Sells an OTM put (ATM-1) and uses that premium to buy an OTM call (ATM+1). Since both options are out of the money, the premiums are often close, making this a near-zero-cost trade. You profit as Nifty rises above the call strike, and lose as it falls below the put strike. Between the two strikes, the trade is roughly flat.

Think of it as a directional bet where you fund the upside participation by giving up downside protection. You don't pay much to enter, but your loss is unlimited if Nifty falls sharply.

**Example:**
- Nifty is at 23,100. Sell 23050 PE (₹95), Buy 23150 CE (₹110). Net debit = ₹15.
- Nifty rises to 23,400 at expiry → call gains ₹250, put expires worthless, profit = 250 − 15 = **₹235 per unit**
- Nifty falls to 22,800 at expiry → call expires worthless, put loses ₹250, loss = 250 + 15 = **₹265 per unit**
- Nifty closes between 23,050 and 23,150 at expiry → both expire worthless, loss = **₹15** (net debit paid)

```
You profit when : Nifty closes above 23,165 (call strike + net debit)
Max profit      : Grows as Nifty rises above the call strike — no cap
Max loss        : Grows as Nifty falls below the put strike — no cap
```

> **Range Forward vs Buy Call:** Range forward costs far less (often near zero) but creates downside risk if the market falls sharply. Buy call has capped loss at the premium paid but costs more upfront.

**Run:**
```bash
python3 code/range_forward.py
```
