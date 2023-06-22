pragma solidity ^0.8.10;
pragma experimental ABIEncoderV2;

import {IERC20} from '../../../lib/aave-v3-core/contracts/dependencies/openzeppelin/contracts/IERC20.sol';
import {IAToken} from "../../../lib/aave-v3-core/contracts/interfaces/IAToken.sol";

contract SymbolicLendingPool {

struct ReserveConfigurationMap {
    //bit 0-15: LTV
    //bit 16-31: Liq. threshold
    //bit 32-47: Liq. bonus
    //bit 48-55: Decimals
    //bit 56: reserve is active
    //bit 57: reserve is frozen
    //bit 58: borrowing is enabled
    //bit 59: stable rate borrowing enabled
    //bit 60: asset is paused
    //bit 61: borrowing in isolation mode is enabled
    //bit 62-63: reserved
    //bit 64-79: reserve factor
    //bit 80-115 borrow cap in whole tokens, borrowCap == 0 => no cap
    //bit 116-151 supply cap in whole tokens, supplyCap == 0 => no cap
    //bit 152-167 liquidation protocol fee
    //bit 168-175 eMode category
    //bit 176-211 unbacked mint cap in whole tokens, unbackedMintCap == 0 => minting disabled
    //bit 212-251 debt ceiling for isolation mode with (ReserveConfiguration::DEBT_CEILING_DECIMALS) decimals
    //bit 252-255 unused

    uint256 data;
  }

    struct ReserveData {
    //stores the reserve configuration
    ReserveConfigurationMap configuration;
    //the liquidity index. Expressed in ray
    uint128 liquidityIndex;
    //the current supply rate. Expressed in ray
    uint128 currentLiquidityRate;
    //variable borrow index. Expressed in ray
    uint128 variableBorrowIndex;
    //the current variable borrow rate. Expressed in ray
    uint128 currentVariableBorrowRate;
    //the current stable borrow rate. Expressed in ray
    uint128 currentStableBorrowRate;
    //timestamp of last update
    uint40 lastUpdateTimestamp;
    //the id of the reserve. Represents the position in the list of the active reserves
    uint16 id;
    //aToken address
    address aTokenAddress;
    //stableDebtToken address
    address stableDebtTokenAddress;
    //variableDebtToken address
    address variableDebtTokenAddress;
    //address of the interest rate strategy
    address interestRateStrategyAddress;
    //the current treasury balance, scaled
    uint128 accruedToTreasury;
    //the outstanding unbacked aTokens minted through the bridging feature
    uint128 unbacked;
    //the outstanding debt borrowed against this asset in isolation mode
    uint128 isolationModeTotalDebt;
  }
    // an underlying asset in the pool
    IERC20 public underlyingToken;
    // the aToken associated with the underlying above
    IAToken public aToken;
    // This index is used to convert the underlying token to its matching
    // AToken inside the pool, and vice versa.
    mapping (uint256 => uint256) public liquidityIndex;

    ReserveData internal data;

    /**
     * @dev Deposits underlying token in the Atoken's contract on behalf of the user,
            and mints Atoken on behalf of the user in return.
     * @param asset The underlying sent by the user and to which Atoken shall be minted
     * @param amount The amount of underlying token sent by the user
     * @param onBehalfOf The recipient of the minted Atokens
     * @param referralCode A unique code (unused)
     **/
    function deposit(
        address asset,
        uint256 amount,
        address onBehalfOf,
        uint16 referralCode
    ) external {
        require(asset == address(underlyingToken));
        underlyingToken.transferFrom(
            msg.sender,
            address(aToken),
            amount
        );
        aToken.mint(
            msg.sender,
            onBehalfOf,
            amount,
            liquidityIndex[block.timestamp]
        );
    }

    /**
     * @dev Burns Atokens in exchange for underlying asset
     * @param asset The underlying asset to which the Atoken is connected
     * @param amount The amount of underlying tokens to be burned
     * @param to The recipient of the burned Atokens
     * @return The `amount` of tokens withdrawn
     **/
    function withdraw(
        address asset,
        uint256 amount,
        address to
    ) external returns (uint256) {
        require(asset == address(underlyingToken));
        aToken.burn(
            msg.sender,
            to,
            amount,
            liquidityIndex[block.timestamp]
        );
        return amount;
    }

    /**
     * @dev A simplification returning a constant
     * @param asset The underlying asset to which the Atoken is connected
     * @return liquidityIndex the `liquidityIndex` of the asset
     **/
    function getReserveNormalizedIncome(address asset)
        external
        virtual
        returns (uint256)
    {
        require(asset == address(underlyingToken));
        return liquidityIndex[block.timestamp];
    }

    function finalizeTransfer(
        address asset,
        address from,
        address to,
        uint256 amount,
        uint256 balanceFromBefore,
        uint256 balanceToBefore
    ) external virtual {return;}

    function getReserveData(address asset)
        external
        view
    returns (ReserveData memory) {
        ReserveData memory cache = data;
        cache.aTokenAddress = address(aToken);
        return cache;
    }
}
