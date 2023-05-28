import "StaticATokenLM_base.spec"

// xuwinnie : properties related to rewards ... I mean contest rewards

/////////////////// CATCHER ////////////////////////
// can not redeem more than balance of pool
rule maxRedeemUnderlying_bug9 (env e, address a) {
    uint maxRedeem = maxRedeemUnderlying (e,a);
    assert convertToAssets(e,maxRedeem) <= _DummyERC20_aTokenUnderlying.balanceOf(_AToken); 
}

// balance of Atoken should decrease as expect
// takes more than 1 hour
rule mintShares_bug6 (env e, address a, address b) {
    require e.msg.sender == a;
    require(getSelf()) != a;
    uint shares;
    mathint beforeATokenBalance = _AToken.balanceOf(e,a);
    mint(e,shares,b);
    mathint afterATokenBalance = _AToken.balanceOf(e,a);
    mathint shouldDecrease = previewMint(e,shares);

    // aToken balance is magical, so we specify the rate and weaken the assertion
    require rate(e) == 2 * RAY();
    assert beforeATokenBalance - shouldDecrease + 2 >= afterATokenBalance;
    assert beforeATokenBalance - shouldDecrease - 2 <= afterATokenBalance;
}

// as its name
rule transferNeverDecreaseReward_bug1 (env e, address reward) {
    address a; address b; uint n;
    single_RewardToken_setup();
    require reward == _DummyERC20_rewardToken;
    require a!= 0;
    require b!= 0;

    mathint aBefore = getClaimableRewards(e,a,reward);
    mathint bBefore = getClaimableRewards(e,b,reward);
    transferFrom(e,a,b,n);
    mathint aAfter = getClaimableRewards(e,a,reward);
    mathint bAfter = getClaimableRewards(e,b,reward);

    assert aBefore <= aAfter;
    assert bBefore <= bAfter;
}

/////////////////// NO BACKDOOR ////////////////////////
// no backdoor function
// sanity check will and should fail
rule noBackdoor {
    method f; env e; calldataarg arg;
    require(!AllFunctions(f));
    f@withrevert(e,arg);
    assert lastReverted;
}

////////////////// EQUIVALENCE //////////////////////
// diffrent approach to deposit have the same effect
rule depositEquivalence {
    storage init = lastStorage;

    env e_2; uint256 assets_2; address recipient_2; uint16 referralCode_2; bool fromUnderlying_2;
    deposit(e_2, assets_2, recipient_2, referralCode_2, fromUnderlying_2) at init;
    storage result_2 = lastStorage;

    env e_3; uint256 assets_3; address receiver_3;
    deposit(e_3, assets_3, receiver_3) at init;
    storage result_3 = lastStorage;

    address a;
    // to simplify computing 
    require(a == e_3.msg.sender || a == receiver_3);

    mathint balance_2 = balanceOf(a) at result_2;
    mathint balance_3 = balanceOf(a) at result_3;

    require(e_2.block.timestamp == e_3.block.timestamp);
    require(e_2.msg.sender == e_3.msg.sender);
    require(recipient_2 == receiver_3);
    require(assets_2 == assets_3);
    assert(balance_2 == balance_3);
}

///////////////// USER ///////////////////////
// as its name
rule balanceRiseAfterDeposit(env e, address a, uint assets) {
    mathint shouldIncrease = convertToShares(e,assets);
    mathint beforeBalance = balanceOf(a);
    mathint returnedIncrease = deposit(e,assets,a);
    mathint afterBalance = balanceOf(a);
    mathint actuallyIncrease = afterBalance - beforeBalance;

    require NotTooLarge(shouldIncrease);
    require NotTooLarge(beforeBalance);

    assert returnedIncrease == shouldIncrease;
    assert actuallyIncrease == shouldIncrease;
}

// as its name
rule balanceWillNotGoDownWhenOtherDeposit(address a) {
    mathint beforeBalance = balanceOf(a);

    env e; uint256 assets; address receiver;
    deposit(e, assets, receiver);
    require(e.msg.sender != a);
    require(receiver != a);
    require(allowance(a,e.msg.sender) == 0);

    mathint afterBalance = balanceOf(a);

    assert beforeBalance == afterBalance;
}

// as its name
rule balanceWillNotGoDownWhenOtherWithdraw(address a) {
    mathint beforeBalance = balanceOf(a);

    env e; uint256 assets; address receiver; address owner;
    require(allowance(a,e.msg.sender) == 0);
    require(e.msg.sender != a);
    require(receiver != a);
    withdraw(e, assets, receiver, owner);

    mathint afterBalance = balanceOf(a);

    assert beforeBalance == afterBalance;
}

// just for fun
rule chenji {
    mathint x; mathint y; mathint z;
    assert x*x+y*y+z*z>=x*y+y*z+z*x;
}