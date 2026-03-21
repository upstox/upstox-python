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

---

## Bear Butterfly — [code/bear_butterfly.py](code/bear_butterfly.py)

**When to use:** You expect Nifty to fall to a specific level by expiry — not too much, not too little. You want a low-cost trade with a sharp profit peak exactly at your target price.

**What it does:** Uses three put strikes — buy one ATM put, sell two ATM-1 puts, and buy one ATM-2 put. The two sold puts bring in premium that makes this significantly cheaper than a plain bear put spread. Maximum profit is earned when Nifty closes exactly at ATM-1 (the middle strike) at expiry. Both max profit and max loss are fully capped.

Think of it as a sniper trade on the downside — very low cost, defined risk, but Nifty needs to land close to your middle strike for the best payout.

**Example:**
- Nifty is at 23,100. Buy 23100 PE (₹130), Sell 2× 23050 PE (₹95 each), Buy 23000 PE (₹65).
- Net cost = (130 + 65) − (95 × 2) = **₹5 per unit**
- Nifty closes at 23,050 at expiry → max profit = spread width − net cost = 50 − 5 = **₹45 per unit**
- Nifty stays at 23,100 or above → all puts expire worthless, you lose **₹5**
- Nifty falls to 23,000 or below → gains and losses cancel out, you lose **₹5**

```
You profit when : Nifty closes between 23,005 and 23,095 (approx)
Max profit      : ₹45 per unit — if Nifty closes exactly at 23,050 (ATM-1)
Max loss        : ₹5 per unit — the small net premium you paid
```

> **Why use this over a Bear Put Spread?** Much cheaper entry. The trade-off is that your profit is concentrated at one specific price — the middle strike.

**Run:**
```bash
python3 code/bear_butterfly.py
```

---

## Bear Condor — [code/bear_condor.py](code/bear_condor.py)

**When to use:** You expect Nifty to fall moderately into a specific range — not just a tiny dip, but not a full crash either. You want defined risk at a lower cost than a simple put spread.

**What it does:** Uses four put strikes in descending order — buy ATM put, sell ATM-1 and ATM-2 puts, buy ATM-3 put. The two short puts in the middle bring in premium that reduces your net cost. Maximum profit is earned when Nifty closes anywhere between the two short strikes (ATM-1 and ATM-2) at expiry. Both max profit and max loss are fully capped.

Think of it as a bear put spread with an extra layer — a wider profit zone than the butterfly, at a slightly higher cost.

**Example:**
- Nifty is at 23,100. Buy 23100 PE (₹130), Sell 23050 PE (₹95), Sell 23000 PE (₹65), Buy 22950 PE (₹40).
- Net cost = (130 + 40) − (95 + 65) = **₹10 per unit**
- Nifty closes between 23,050 and 23,000 at expiry → max profit = spread width − net cost = 50 − 10 = **₹40 per unit**
- Nifty stays at 23,100 or above → all puts expire worthless, you lose **₹10**
- Nifty falls to 22,950 or below → all spreads cancel out, you lose **₹10**

```
You profit when : Nifty closes between 23,090 and 22,960 (approx)
Max profit      : ₹40 per unit — if Nifty closes between 23,050 and 23,000
Max loss        : ₹10 per unit — the net premium you paid
```

> **Why use this over a Bear Butterfly?** Wider profit zone — you don't need Nifty to land on one exact strike. You sacrifice a little profit but get more room for the trade to work.

**Run:**
```bash
python3 code/bear_condor.py
```

---

## Long Calendar with Puts — [code/long_calendar_put.py](code/long_calendar_put.py)

**When to use:** You expect Nifty to stay near its current level in the short term but fall over the coming week. You want to use time decay to your advantage.

**What it does:** Sells a current-week ATM put and buys a next-week ATM put at the same strike. The near-term put loses value faster (time decay accelerates closer to expiry), so you profit from that decay while still holding a longer-dated put that benefits if Nifty falls after the near-term expiry.

Think of it as a two-phase trade — first earn from the near-term option expiring worthless, then ride any downside through the longer-dated put you still own.

**Example:**
- Nifty is at 23,100. Sell current-week 23100 PE for ₹60, Buy next-week 23100 PE for ₹130. Net cost = ₹70.
- Nifty stays near 23,100 through current-week expiry → near-term put expires worthless, you keep ₹60. You still own the next-week put worth ₹130 (or more if Nifty falls).
- Nifty falls to 22,800 after current-week expiry → next-week put gains value significantly, overall profit grows.
- Nifty rises sharply → both puts lose value, max loss is the ₹70 net cost you paid.

```
You profit when : Nifty stays near ATM through near-term expiry, then falls
Max profit      : Varies — depends on how much the far-term put gains after near-term expires
Max loss        : ₹70 per unit — the net premium you paid (difference between the two puts)
```

> **Key difference from other strategies:** This trade spans two expiries. You are not just betting on direction — you are also betting on *when* the move happens.

**Run:**
```bash
python3 code/long_calendar_put.py
```

---

## Short Synthetic Future — [code/short_synthetic_future.py](code/short_synthetic_future.py)

**When to use:** You have a strong bearish view and want the same profit/loss profile as selling a futures contract, but using options instead.

**What it does:** Sells an ATM call and buys an ATM put at the same strike and expiry. The premium collected from the sold call partially offsets the cost of the bought put, making this a near-zero-cost position. From this point, the trade behaves exactly like a short futures position — you profit point-for-point as Nifty falls, and lose point-for-point as it rises.

Think of it as a short futures position built from options. You get the same unlimited downside profit and unlimited upside loss, but without daily MTM settlement like futures.

**Example:**
- Nifty is at 23,100. Sell 23100 CE for ₹150, Buy 23100 PE for ₹130. Net credit = ₹20.
- Nifty falls to 22,700 at expiry → put pays ₹400, call expires worthless, profit = 400 + 20 = **₹420 per unit**
- Nifty rises to 23,500 at expiry → call is exercised against you, put expires worthless, loss = 400 − 20 = **₹380 per unit**
- Nifty closes exactly at 23,100 → both expire worthless, you keep the **₹20** net credit

```
You profit when : Nifty closes below 23,120 (strike + net credit)
Max profit      : Grows point-for-point as Nifty falls — no cap
Max loss        : Grows point-for-point as Nifty rises — no cap
```

> **How is this different from just shorting a futures contract?** The payoff is identical, but you avoid daily mark-to-market settlements. However, the risk is just as large — always use a clear stop-loss plan before entering.

**Run:**
```bash
python3 code/short_synthetic_future.py
```

---

## Put Ratio Back Spread — [code/put_ratio_back_spread.py](code/put_ratio_back_spread.py)

**When to use:** You expect a sharp, significant fall in Nifty. You want to benefit from a big downside move while keeping entry cost low — ideally entering for free or a small credit.

**What it does:** Sells one ATM put and uses that premium to buy two OTM puts (ATM-1). The sold ATM put finances most or all of the cost of the two bought puts. The trade has a zone of maximum loss around the short strike but profits substantially if Nifty falls sharply below the long put strikes. If Nifty stays flat or rises, you keep the small net credit (if any).

Think of it as paying for a big downside move with the premium collected from selling a closer put. The more Nifty falls, the more you profit — because you hold two long puts.

**Example:**
- Nifty is at 23,100. Sell 23100 PE (₹130), Buy 2× 23050 PE (₹95 each). Net credit = ₹130 − ₹190 = **−₹60 net debit** (or credit depending on premiums).
- Nifty closes at 23,050 at expiry → short put loses ₹50, long puts expire worthless, loss = 50 + 60 = **₹110** (max loss zone)
- Nifty falls to 22,800 at expiry → short put loses ₹300, 2 long puts gain 2×250 = ₹500, net = 500 − 300 − 60 = **₹140 profit**
- Nifty stays above 23,100 at expiry → all puts expire worthless, loss = **₹60** (net debit paid)

```
You profit when : Nifty falls significantly below ATM-1 strike
Max profit      : Grows as Nifty falls sharply — 2 long puts accelerate gains
Max loss        : At the long put strike (ATM-1) — limited, predictable zone
```

> **Put Ratio Back Spread vs Buy Put:** Back spread profits much more on a large crash due to 2× long puts, at a lower entry cost. The trade-off is a loss zone near the short strike if Nifty falls only slightly.

**Run:**
```bash
python3 code/put_ratio_back_spread.py
```

---

## Risk Reversal — [code/risk_reversal.py](code/risk_reversal.py)

**When to use:** You have a clear bearish view and want downside exposure at very low cost — or even for free — by funding the put with a sold call.

**What it does:** Sells an OTM call (ATM+1) and uses that premium to buy an OTM put (ATM-1). Since both options are out of the money, the premiums are often close, making this a near-zero-cost trade. You profit as Nifty falls below the put strike, and lose as it rises above the call strike. Between the two strikes, the trade is roughly flat.

Think of it as a directional bet where you fund the downside protection by giving up upside participation. You don't pay much to enter, but your loss is unlimited if Nifty rallies.

**Example:**
- Nifty is at 23,100. Sell 23150 CE (₹110), Buy 23050 PE (₹95). Net credit = ₹15.
- Nifty falls to 22,800 at expiry → put gains ₹250, call expires worthless, profit = 250 + 15 = **₹265 per unit**
- Nifty rises to 23,400 at expiry → call loses ₹250, put expires worthless, loss = 250 − 15 = **₹235 per unit**
- Nifty closes between 23,050 and 23,150 at expiry → both expire worthless, profit = **₹15** (net credit kept)

```
You profit when : Nifty closes below 23,035 (put strike − net credit)
Max profit      : Grows as Nifty falls below the put strike — no cap
Max loss        : Grows as Nifty rises above the call strike — no cap
```

> **Risk Reversal vs Buy Put:** Risk reversal costs far less (often near zero) but gives up upside if the market rallies sharply. Buy put has capped loss at the premium paid but costs more upfront.

**Run:**
```bash
python3 code/risk_reversal.py
```
