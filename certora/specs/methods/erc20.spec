// erc20 methods
methods {
    name()                                returns (string)  =>  DISPATCHER(true)
    symbol()                              returns (string)  =>  DISPATCHER(true)
    decimals()                            returns (uint8)   =>  DISPATCHER(true)
    totalSupply()                         returns (uint256) envfree 
    balanceOf(address)                    returns (uint256) envfree 
    allowance(address,address)            returns (uint)    envfree 
    approve(address,uint256)              returns (bool)    
    transfer(address,uint256)             returns (bool)    
    transferFrom(address,address,uint256) returns (bool)    
}
