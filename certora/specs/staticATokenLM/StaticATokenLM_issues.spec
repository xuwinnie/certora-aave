import "StaticATokenLM_base.spec"

rule noMoreThanMaxRedeemUnderlying_strong (env e, address a, address b) {
    mathint maxRedeem = maxRedeemUnderlying (e,a);
    require (maxRedeem != 0);

    require rate(e) >= RAY();
    require rate(e) <= 2 * RAY();

    uint inputShares; uint actualRedeemshare; uint actualWithdrawAmount;
    actualRedeemshare, actualWithdrawAmount = redeem(e,inputShares,b,a,true);
    assert inputShares <= maxRedeem;
}

rule noMoreThanMaxRedeemUnderlying_stronger (env e, address a, address b) {
    mathint maxRedeem = maxRedeemUnderlying (e,a);
    require (maxRedeem != 0);

    require rate(e) >= RAY();
    require rate(e) <= 2 * RAY();

    uint inputShares; uint actualRedeemshare; uint actualWithdrawAmount;
    actualRedeemshare, actualWithdrawAmount = redeem(e,inputShares,b,a,true);
    assert actualRedeemshare <= maxRedeem;
}