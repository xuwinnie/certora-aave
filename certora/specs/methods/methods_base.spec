import "erc20.spec"

using StaticATokenLMHarness as _StaticATokenLM
using SymbolicLendingPool as _SymbolicLendingPool
using RewardsControllerHarness as _RewardsController
using TransferStrategyHarness as _TransferStrategy
using DummyERC20_aTokenUnderlying as _DummyERC20_aTokenUnderlying 
using AToken as _AToken
using DummyERC20_rewardToken as _DummyERC20_rewardToken 

/////////////////// Methods ////////////////////////

methods
{
    // static aToken
	// -------------
        asset() returns (address)
        totalAssets() returns (uint256)
        maxWithdraw(address owner) returns (uint256)
        maxRedeem(address owner) returns (uint256)
        previewWithdraw(uint256) returns (uint256)
        previewDeposit(uint256) returns (uint256)
        previewRedeem(uint256) returns (uint256)
        maxDeposit(address) returns (uint256)
        previewMint(uint256) returns (uint256)
        maxMint(address) returns (uint256)
        rate() returns (uint256)
        getUnclaimedRewards(address, address) returns (uint256) envfree
        rewardTokens() returns (address[]) envfree
        isRegisteredRewardToken(address) returns (bool) envfree
        metaDeposit(address,address,uint256,uint16,bool,uint256,_StaticATokenLM.SignatureParamsHarness,_StaticATokenLM.PermitParamsHarness) returns (uint256)
        
    // static aToken harness
    // ---------------------
        getATokenUnderlying() returns (address)
        getRewardsIndexOnLastInteraction(address, address) returns (uint128) envfree
        getRewardTokensLength() returns (uint256) envfree 
        getRewardToken(uint256) returns (address) envfree
        getAToken() returns (address)
        getSelf() returns (address) envfree

    // pool
    // ----
        _SymbolicLendingPool.getReserveNormalizedIncome(address) returns (uint256)

    // rewards controller
	// ------------------
        // In RewardsDistributor.sol called by RewardsController.sol
        getAssetIndex(address, address) returns (uint256, uint256)
        // In ScaledBalanceTokenBase.sol called by getAssetIndex
        scaledTotalSupply() returns (uint256)   
        // Called by RewardsController._transferRewards()
        // Defined in TransferStrategyHarness as simple transfer() 
        performTransfer(address,address,uint256) returns (bool) =>  DISPATCHER(true)

        // harness methods of the rewards controller
        _RewardsController.getRewardsIndex(address,address)returns (uint256) envfree
        _RewardsController.getAvailableRewardsCount(address) returns (uint128) envfree
        _RewardsController.getRewardsByAsset(address, uint128) returns (address) envfree
        _RewardsController.getAssetListLength() returns (uint256) envfree
        _RewardsController.getAssetByIndex(uint256) returns (address) envfree
        _RewardsController.getDistributionEnd(address, address)  returns (uint256) envfree
        _RewardsController.getUserAccruedRewards(address, address) returns (uint256) envfree
        _RewardsController.getUserAccruedReward(address, address, address) returns (uint256) envfree
        _RewardsController.getAssetDecimals(address) returns (uint8) envfree
        _RewardsController.getRewardsData(address,address) returns (uint256,uint256,uint256,uint256) envfree
        _RewardsController.getUserAssetIndex(address,address, address) returns (uint256) envfree

    // underlying token
    // ----------------
        _DummyERC20_aTokenUnderlying.balanceOf(address) returns(uint256) envfree

    // aToken
	// ------
        _AToken.balanceOf(address) returns (uint256)
        _AToken.totalSupply() returns (uint256) envfree
        _AToken.allowance(address, address) returns (uint256) envfree
        _AToken.UNDERLYING_ASSET_ADDRESS() returns (address) envfree
        _AToken.scaledBalanceOf(address) returns (uint256) envfree
        _AToken.scaledTotalSupply() returns (uint256) envfree
        
        // called in aToken
        finalizeTransfer(address, address, address, uint256, uint256, uint256) => NONDET  
        // Called by rewardscontroller.sol
        // Defined in scaledbalancetokenbase.sol
        getScaledUserBalanceAndSupply(address) returns (uint256, uint256) 

    // reward token
    // ------------
        _DummyERC20_rewardToken.balanceOf(address) returns (uint256) envfree
        _DummyERC20_rewardToken.totalSupply() returns (uint256) envfree

        UNDERLYING_ASSET_ADDRESS() returns (address) envfree => CONSTANT UNRESOLVED
 }

///////////////// DEFINITIONS //////////////////////

    definition RAY() returns uint256 = 10^27;

    definition NotTooLarge(uint256 n) returns bool = (n <= 2^100);

    definition BalanceDisturbingFunctions(method f) returns bool = 
        (f.selector == metaDeposit(address,address,uint256,uint16,bool,uint256,(address,address,uint256,uint256,uint8,bytes32,bytes32),(uint8,bytes32,bytes32)).selector ||
        f.selector == metaWithdraw(address,address,uint256,uint256,bool,uint256,(uint8,bytes32,bytes32)).selector ||
        f.selector == deposit(uint256,address,uint16,bool).selector ||
        f.selector == redeem(uint256,address,address,bool).selector ||
        f.selector == deposit(uint256,address).selector ||
        f.selector == mint(uint256,address).selector ||
        f.selector == withdraw(uint256,address,address).selector ||
        f.selector == redeem(uint256,address,address).selector);

    definition ERC20Functions(method f) returns bool =
        (f.selector == transfer(address,uint256).selector ||
        f.selector == transferFrom(address,address,uint256).selector ||
        f.selector == approve(address,uint256).selector ||
        f.selector == permit(address,address,uint256,uint256,uint8,bytes32,bytes32).selector);

    /// @notice Claim rewards methods
    definition claimFunctions(method f) returns bool = 
        (f.selector == claimRewardsToSelf(address[]).selector ||
        f.selector == claimRewards(address, address[]).selector ||
        f.selector == claimRewardsOnBehalf(address, address,address[]).selector);
                
    definition collectAndUpdateFunction(method f) returns bool =
        f.selector == collectAndUpdateRewards(address).selector;

    definition harnessOnlyMethods(method f) returns bool =
        (harnessMethodsMinusHarnessClaimMethods(f) ||
        f.selector == claimSingleRewardOnBehalf(address, address, address).selector ||
        f.selector == claimDoubleRewardOnBehalfSame(address, address, address).selector);
        
    definition harnessMethodsMinusHarnessClaimMethods(method f) returns bool =
        (f.selector == getATokenUnderlying().selector ||
        f.selector == getAToken().selector ||
        f.selector == getSelf().selector ||
        f.selector == getRewardTokensLength().selector ||
        f.selector == getRewardToken(uint256).selector ||
        f.selector == getRewardsIndexOnLastInteraction(address, address).selector ||
        f.selector == getLastUpdatedIndex(address).selector);

    definition AllFunctions(method f) returns bool = 
        (f.selector == constructor(address,address).selector ||
        f.selector == nonces(address).selector ||
        f.selector == name().selector ||
        f.selector == previewRedeem(uint256).selector ||
        f.selector == refreshRewardTokens().selector ||
        f.selector == getClaimableRewards(address,address).selector ||
        f.selector == asset().selector ||
        f.selector == STATIC__ATOKEN_LM_REVISION().selector ||
        f.selector == convertToShares(uint256).selector ||
        f.selector == totalAssets().selector ||
        f.selector == deposit(uint256,address,uint16,bool).selector ||
        f.selector == withdraw(uint256,address,address).selector ||
        f.selector == redeem(uint256,address,address,bool).selector ||
        f.selector == getCurrentRewardsIndex(address).selector ||
        f.selector == METAWITHDRAWAL_TYPEHASH().selector ||
        f.selector == DOMAIN_SEPARATOR().selector ||
        f.selector == claimDoubleRewardOnBehalfSame(address,address,address).selector ||
        f.selector == rewardTokens().selector ||
        f.selector == aTokenUnderlying().selector ||
        f.selector == claimRewards(address,address[]).selector ||
        f.selector == INCENTIVES_CONTROLLER().selector ||
        f.selector == isRegisteredRewardToken(address).selector ||
        f.selector == getLastUpdatedIndex(address).selector ||
        f.selector == getUnclaimedRewards(address,address).selector ||
        f.selector == claimRewardsToSelf(address[]).selector ||
        f.selector == rate().selector ||
        f.selector == maxWithdraw(address).selector ||
        f.selector == balanceOf(address).selector ||
        f.selector == approve(address,uint256).selector ||
        f.selector == maxMint(address).selector ||
        f.selector == METADEPOSIT_TYPEHASH().selector ||
        f.selector == previewMint(uint256).selector ||
        f.selector == convertToAssets(uint256).selector ||
        f.selector == transfer(address,uint256).selector ||
        f.selector == getAToken().selector ||
        f.selector == allowance(address,address).selector ||
        f.selector == symbol().selector ||
        f.selector == maxDepositUnderlying(address).selector ||
        f.selector == getATokenUnderlying().selector ||
        f.selector == POOL().selector ||
        f.selector == getRewardsIndexOnLastInteraction(address,address).selector ||
        f.selector == initialize(address,string,string).selector ||
        f.selector == collectAndUpdateRewards(address).selector ||
        f.selector == mint(uint256,address).selector ||
        f.selector == permit(address,address,uint256,uint256,uint8,bytes32,bytes32).selector ||
        f.selector == redeem(uint256,address,address).selector ||
        f.selector == claimRewardsOnBehalf(address,address,address[]).selector ||
        f.selector == metaDeposit(address,address,uint256,uint16,bool,uint256,(address,address,uint256,uint256,uint8,bytes32,bytes32),(uint8,bytes32,bytes32)).selector ||
        f.selector == getRewardTokensLength().selector ||
        f.selector == getTotalClaimableRewards(address).selector ||
        f.selector == getSelf().selector ||
        f.selector == claimSingleRewardOnBehalf(address,address,address).selector ||
        f.selector == getRewardToken(uint256).selector ||
        f.selector == previewDeposit(uint256).selector ||
        f.selector == aToken().selector ||
        f.selector == maxRedeemUnderlying(address).selector ||
        f.selector == transferFrom(address,address,uint256).selector ||
        f.selector == totalSupply().selector ||
        f.selector == deposit(uint256,address).selector ||
        f.selector == decimals().selector ||
        f.selector == previewWithdraw(uint256).selector ||
        f.selector == metaWithdraw(address,address,uint256,uint256,bool,uint256,(uint8,bytes32,bytes32)).selector ||
        f.selector == maxDeposit(address).selector ||
        f.selector == maxRedeem(address).selector);

////////////////// FUNCTIONS //////////////////////

    /**
    * @title Single reward setup
    * Setup the `StaticATokenLM`'s rewards so they contain a single reward token
    * which is` _DummyERC20_rewardToken`.
    */
    function single_RewardToken_setup() {
        require getRewardTokensLength() == 1;
        require getRewardToken(0) == _DummyERC20_rewardToken;
    }

    function zero_RewardToken_setup() {
        require getRewardTokensLength() == 0;
    }

    /**
    * @title Single reward setup in RewardsController
    * Sets (in `_RewardsController`) the first reward for `_AToken` as
    * `_DummyERC20_rewardToken`.
    */
    function rewardsController_reward_setup() {
        require _RewardsController.getAvailableRewardsCount(_AToken) > 0;
        require _RewardsController.getRewardsByAsset(_AToken, 0) == _DummyERC20_rewardToken;
    }

    /// @title Assumptions that should hold in any run
    /// @dev Assume that RewardsController.configureAssets(RewardsDataTypes.RewardsConfigInput[] memory rewardsInput) was called
    function setup(env e, address user)
    {
        require getRewardTokensLength() > 0;
        require _RewardsController.getAvailableRewardsCount(_AToken)  > 0;
        require _RewardsController.getRewardsByAsset(_AToken, 0) == _DummyERC20_rewardToken;
        require currentContract != e.msg.sender;
        require currentContract != user;
    
        require _AToken != user;
        require _RewardsController !=  user;
        require _DummyERC20_aTokenUnderlying  != user;
        require _DummyERC20_rewardToken != user;
        require _SymbolicLendingPool != user;
        require _TransferStrategy != user;
        require _TransferStrategy != user;
    }

