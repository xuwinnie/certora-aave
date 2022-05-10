pragma solidity ^0.8.10;

import {IAaveIncentivesController} from 'aave-v3-core/contracts/interfaces/IAaveIncentivesController.sol';

interface IAToken {
  function getIncentivesController() external view returns (IAaveIncentivesController);

  function UNDERLYING_ASSET_ADDRESS() external view returns (address);
}