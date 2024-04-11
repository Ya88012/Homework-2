# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1
Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).

### My solution:
* profitable path: tokenB->tokenA->tokenD->tokenC->tokenB
* tokenB->tokenA:
    * amountIn: 5
    * amountOut: 5.655321988655323
* tokenA->tokenD:
    * amountIn: 5.655321988655323
    * amountOut: 2.458781317097934
* tokenD->tokenC:
    * amountIn: 2.458781317097934
    * amountOut: 5.0889272933015155
* tokenC->tokenB:
    * amountIn: 5.0889272933015155
    * amountOut: 20.129888944077447
* final reward: 20.129888944077447

## Problem 2
What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

### My solution:
Slippage in Automated Market Makers (AMMs) like Uniswap refers to the price movement caused by large trades. When a large trade executes, it impacts the pool's reserves, resulting in a worse price for the trader.

Uniswap V2 addresses slippage by allowing traders to set a maximum slippage tolerance. If the price moves unfavorably beyond this tolerance, the trade is reverted.

Example in Solidity:

```solidity
function swapExactETHForTokens(uint amountOutMin, address[] calldata path, address to, uint deadline)
        external
        payable
        returns (uint[] memory amounts)
{
    amounts = UniswapV2Library.getAmountsOut(msg.value, path);
    require(amounts[amounts.length - 1] >= amountOutMin, 'UniswapV2Router: INSUFFICIENT_OUTPUT_AMOUNT');
    // ... (rest of the function)
}
```

This function reverts if `amounts[amounts.length - 1]` (the output amount) is less than `amountOutMin` (the user's slippage tolerance).

## Problem 3
Please examine the mint function in the UniswapV2Pair contract. Upon initial liquidity minting, a minimum liquidity is subtracted. What is the rationale behind this design?

### My solution:
In the UniswapV2Pair contract, a small amount of liquidity is subtracted during the initial liquidity minting process. This is done to ensure that the pair has a non-zero liquidity value, even if one of the tokens becomes worthless or has a value of zero.

The rationale behind this design is to prevent potential division-by-zero errors that could occur during calculations involving the pair's reserves. By maintaining a minimum liquidity value, the contract can safely perform arithmetic operations without encountering such errors.

Here's an example of the `mint` function in Solidity:

```solidity
function mint(address to) external lock returns (uint liquidity) {
    (uint112 _reserve0, uint112 _reserve1) = (reserve0, reserve1);
    uint balance0 = IERC20(token0).balanceOf(address(this));
    uint balance1 = IERC20(token1).balanceOf(address(this));
    uint amount0 = balance0.sub(_reserve0);
    uint amount1 = balance1.sub(_reserve1);

    bool feeOn = _mintFee(_reserve0, _reserve1);
    uint _totalSupply = totalSupply;
    if (_totalSupply == 0) {
        liquidity = Math.sqrt(amount0.mul(amount1)).sub(MINIMUM_LIQUIDITY);
        _mint(address(0), MINIMUM_LIQUIDITY); // permanently lock the minimum liquidity
    } else {
        liquidity = Math.min(amount0.mul(_totalSupply) / _reserve0, amount1.mul(_totalSupply) / _reserve1);
    }
    // ... (rest of the function)
}
```

In the above example, during the initial liquidity minting (`_totalSupply == 0`), the `MINIMUM_LIQUIDITY` value is subtracted from the calculated liquidity, and this minimum liquidity is permanently locked by minting it to the zero address (`_mint(address(0), MINIMUM_LIQUIDITY)`).

## Problem 4
Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?

### My solution:
When liquidity is minted in an existing Uniswap V2 pair and it is not the initial liquidity provision, the liquidity tokens are minted proportionally based on the following formula:

```solidity
liquidity = Math.min(amount0.mul(_totalSupply) / _reserve0, amount1.mul(_totalSupply) / _reserve1);
```

The intention behind using this specific formula is to maintain the constant product formula `x * y = k` for the pair's reserves. This ensures that the liquidity provider's share of the total liquidity pool remains proportional to their deposited amounts, preserving the pool's overall ratio of the two tokens.

Here's an intuitive example to understand the reasoning:

Let's say the existing pool has 100 ETH and 1000 USDC reserves, with a total liquidity of 1000 LP tokens. A new liquidity provider wants to deposit 10 ETH and 100 USDC.

If we simply added the new liquidity to the reserves (110 ETH and 1100 USDC), the ratio of the two tokens would change, violating the constant product formula.

Instead, by using the formula `liquidity = Math.min(10 * 1000 / 100, 100 * 1000 / 1000) = 100`, the new liquidity provider receives 100 LP tokens, maintaining the same ratio of ETH to USDC in the pool.

This approach ensures that the value of existing LP tokens is not diluted, and the overall ratio of the two tokens in the pool remains constant, adhering to the constant product formula. It also prevents arbitrage opportunities that could arise if the ratio changes.

## Problem 5
What is a sandwich attack, and how might it impact you when initiating a swap?

### My solution:

A sandwich attack is a type of front-running attack that can occur on decentralized exchanges (DEXs) like Uniswap. It involves an attacker placing two transactions "sandwiching" a victim's transaction to extract value from the victim's trade.

Here's an intuitive example of how a sandwich attack might impact you when initiating a swap:

1. You initiate a swap on Uniswap to trade 1 ETH for USDC.
2. An attacker monitors the mempool (pending transactions) and sees your transaction.
3. Before your transaction is processed, the attacker quickly sends two transactions:
    - The first transaction executes a swap in the opposite direction (USDC to ETH), causing the ETH/USDC price to move unfavorably for you.
    - Immediately after, the attacker's second transaction executes your intended swap (ETH to USDC) at the new, worse price.
4. Your transaction is finally processed, but you receive fewer USDC than expected due to the price manipulation.
5. The attacker then trades back to their original position, profiting from the price difference at your expense.

The impact on you is that you receive less USDC than you would have if the sandwich attack didn't occur, effectively paying a higher price for your desired trade. The attacker profits from this price difference by sandwiching your transaction.

Sandwich attacks are possible due to the transparency of pending transactions on DEXs and the ability to front-run transactions by paying higher gas fees. Mitigations include using DEXs with better front-running resistance mechanisms or trading smaller amounts to reduce the profitability of such attacks.
