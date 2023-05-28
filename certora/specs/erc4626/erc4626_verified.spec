import "erc4626_base.spec"

// The following spec implements erc4626 properties according to the official eip described here:
// https://eips.ethereum.org/EIPS/eip-4626
// xuwinnie : properties not related to rewards

///////////////// View Properties ///////////////////////

//// Consistency ////

// aToken address Consistency
rule aTokenConsistency(env e) {
    address realAToken = getAToken(e);
    address soCalledAToken1 = aToken@withrevert(e);
    assert !lastReverted;
    address soCalledAToken2 = asset@withrevert(e);
    assert !lastReverted;
    assert soCalledAToken1 == realAToken && soCalledAToken2 == realAToken;
}

// aTokenUnderlying address Consistency
rule aTokenUnderlyingConsistency(env e) {
    address realATokenUnderlying = getATokenUnderlying(e);
    address soCalledATokenUnderlying = aTokenUnderlying@withrevert(e);
    assert !lastReverted;
    assert soCalledATokenUnderlying == realATokenUnderlying;
}

//// view functions ////

// correct totalAssets
rule correctTotalAssets(env e) {
    address self = getSelf();
    mathint realTotalAssets = _AToken.balanceOf(e,self);
    mathint soCalledTotalAssets = totalAssets@withrevert(e);
    assert !lastReverted;
    assert soCalledTotalAssets == realTotalAssets;
}

// correct rate
rule correctRate(env e) {
    address a = getATokenUnderlying(e);
    mathint realRate = _SymbolicLendingPool.getReserveNormalizedIncome(e,a);
    mathint returnRate = rate@withrevert(e);
    assert !lastReverted;
    assert returnRate == realRate;
}

// correct conversion
rule correctConvertToShares (env e) {
    mathint _rate = rate(e);
    require e.msg.value == 0;
    require _rate != 0;
    uint a;
    require a*RAY()<=max_uint;
    mathint b=convertToShares@withrevert(e,a);
    assert !lastReverted;
    assert b*_rate<=a*RAY();
    assert (b+1)*_rate>a*RAY();
}

// correct conversion
rule correctConvertToAssets (env e) {
    mathint _rate = rate(e);
    require e.msg.value == 0;
    require _rate != 0;
    uint c;
    require c*_rate<=max_uint;
    mathint d=convertToAssets@withrevert(e,c);
    assert !lastReverted;
    assert c*_rate>=d*RAY();
    assert c*_rate<(d+1)*RAY();
}

// balanceOf will not revert
rule reliableBalance (address a) {
    balanceOf@withrevert(a);
    assert !lastReverted;
}

// correct MaxDeposit
rule correctMaxDeposit (env e, address r) {
    require e.msg.value == 0;
    mathint a = maxDeposit@withrevert(e,r);
    assert !lastReverted;
    assert a == max_uint;
}

// correct MaxMint
rule correctMaxMint (env e, address r) {
    require e.msg.value == 0;
    mathint b = maxMint@withrevert(e,r);
    assert !lastReverted;
    assert b == max_uint;
}

// correct MaxWithdraw
rule correctMaxWithdraw (env e, address r) {
    mathint realC = convertToAssets(e,balanceOf(r));
    mathint c = maxWithdraw@withrevert(e,r);
    assert !lastReverted;
    assert c == realC;
}

// correct MaxRedeem
rule correctMaxRedeem (env e, address r) {
    require e.msg.value == 0;
    mathint realD = balanceOf(r);
    mathint d = maxRedeem@withrevert(e,r);
    assert !lastReverted;
    assert d == realD;
}

// correct PreviewDeposit
rule correctPreviewDeposit (env e, uint u) {
    mathint _rate = rate(e);
    require _rate != 0;
    require e.msg.value == 0;
    require NotTooLarge(u);
    require NotTooLarge(_rate);
    mathint realA = convertToShares(e,u);
    uint a = previewDeposit@withrevert(e,u);
    assert !lastReverted;
    assert a == realA;
}

// correct PreviewMint
rule correctPreviewMint (env e, uint u) {
    mathint _rate = rate(e);
    require _rate != 0;
    require e.msg.value == 0;
    require NotTooLarge(u);
    require NotTooLarge(_rate);
    uint b = previewMint@withrevert(e,u);
    assert !lastReverted;
    assert convertToShares(e,b)>=u;
    assert convertToShares(e,b-1)<u;
}

// correct PreviewWithdraw
rule correctPreviewWithdraw (env e, uint u) {
    mathint _rate = rate(e);
    require _rate != 0;
    require e.msg.value == 0;
    require NotTooLarge(u);
    require NotTooLarge(_rate);
    uint c = previewWithdraw@withrevert(e,u);
    assert !lastReverted;
    assert convertToAssets(e,c)>=u;
    assert c>0 => convertToAssets(e,c-1)<u;
}

// correct PreviewRedeem
rule correctPreviewRedeem (env e, uint u) {
    mathint _rate = rate(e);
    require _rate != 0;
    require e.msg.value == 0;
    require NotTooLarge(u);
    require NotTooLarge(_rate);
    mathint realD = convertToAssets(e,u);
    uint d = previewRedeem@withrevert(e,u);
    assert !lastReverted;
    assert d == realD;
}

///////////////// State Properties //////////////////////
// TODO NEXT TIME :)

///////////////// Action Properties ///////////////////////
// balance decrease as expect
rule withdraw (env e, address a, uint assets) {
    mathint beforebalance = balanceOf(a);
    mathint shouldDecrease = previewWithdraw(e,assets);
    withdraw(e,assets,a,a);
    mathint afterbalance = balanceOf(a);
    assert beforebalance - shouldDecrease == afterbalance;
}
