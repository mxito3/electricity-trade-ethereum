pragma solidity ^0.4.21;

contract owned {
    address public owner;
    mapping(address => bool) public isAdmin;
    function owned() public {
        owner = msg.sender;
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }
    //转移所有权
    function transferOwnership(address newOwner) onlyOwner public {
        owner = newOwner;
    }

    function setAdmin(address admin) onlyOwner public
    {
        isAdmin[admin] = true;
    }

    modifier onlyAdmin
    {
        require(isAdmin[msg.sender] == true);
        _;
    }
}

interface tokenRecipient { function receiveApproval(address _from, uint256 _value, address _token, bytes _extraData) external; }


contract TokenERC20 {
    
    string public name;
    string public symbol;
    uint8 public decimals = 0;
    
    uint256 public totalSupply;

  
    mapping (address => uint256) public balanceOf;
    mapping (address => mapping (address => uint256)) public allowance;

    event Transfer(address indexed from, address indexed to, uint256 value);
  
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);

   
    event Burn(address indexed from, uint256 value);

 
    function TokenERC20(
        uint256 initialSupply,
        string tokenName,
        string tokenSymbol
    ) public {
        totalSupply = initialSupply * 10 ** uint256(decimals);  
        balanceOf[msg.sender] = totalSupply;                
        name = tokenName;                                  
        symbol = tokenSymbol;                              
    }

   //内部函数，转币
    function _transfer(address _from, address _to, uint _value) internal {
        
        require(_to != 0x0);
       
        require(balanceOf[_from] >= _value);
        
        require(balanceOf[_to] + _value > balanceOf[_to]);
        
        uint previousBalances = balanceOf[_from] + balanceOf[_to];
        
        balanceOf[_from] -= _value;
        
        balanceOf[_to] += _value;
        emit Transfer(_from, _to, _value);
        
        assert(balanceOf[_from] + balanceOf[_to] == previousBalances);
    }

    
    function transfer(address _from,address _to, uint256 _value) public returns (bool success) {
        _transfer(_from, _to, _value);
        return true;
    }

    //使用授权的币
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        require(_value <= allowance[_from][msg.sender]);    
        _transfer(_from, _to, _value);
        return true;
    }

   //授权
    function approve(address _spender, uint256 _value) public
        returns (bool success) {
        allowance[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }


    function approveAndCall(address _spender, uint256 _value, bytes _extraData)
        public
        returns (bool success) {
        tokenRecipient spender = tokenRecipient(_spender);
        if (approve(_spender, _value)) {
            spender.receiveApproval(msg.sender, _value, this, _extraData);
            return true;
        }
    }

    //销毁
    function burn(uint256 _value) public returns (bool success) {
        require(balanceOf[msg.sender] >= _value);  
        balanceOf[msg.sender] -= _value;            
        totalSupply -= _value;                     
        emit Burn(msg.sender, _value);
        return true;
    }

    //销毁授权的币
    function burnFrom(address _from, uint256 _value) public returns (bool success) {
        require(balanceOf[_from] >= _value);               
        require(_value <= allowance[_from][msg.sender]);   
        balanceOf[_from] -= _value;                        
        allowance[_from][msg.sender] -= _value;           
        totalSupply -= _value;                            
        emit Burn(_from, _value);
        return true;
    }
}



contract MyAdvancedToken is owned, TokenERC20 
{

    uint256 public sellPrice;
    uint256 public buyPrice;

    mapping (address => bool) public frozenAccount;
    mapping (address => uint) public lockedAmount;
    
    event FrozenFunds(address target, bool frozen);
    event Award(address to,uint amount);
    event Punish(address violator,address victim,uint amount);
    event LockToken(address target, uint256 amount,uint lockPeriod);
    event OwnerUnlock(address from,uint256 amount);
    function MyAdvancedToken(
        uint256 initialSupply,
        string tokenName,
        string tokenSymbol
    ) TokenERC20(initialSupply, tokenName, tokenSymbol) public {}

    //转币
    function _transfer(address _from, address _to, uint _value) internal {
        require (_to != 0x0);                               // Prevent transfer to 0x0 address. Use burn() instead
        require (balanceOf[_from] >= _value);               // Check if the sender has enough
        require (balanceOf[_to] + _value >= balanceOf[_to]); // Check for overflows
        require(!frozenAccount[_from]);                     // Check if sender is frozen
        require(!frozenAccount[_to]);                       // Check if recipient is frozen
        balanceOf[_from] -= _value;                         // Subtract from the sender
        balanceOf[_to] += _value;                           // Add the same to the recipient
        emit Transfer(_from, _to, _value);
    }

   //增发
    function mintToken(address target, uint256 mintedAmount) onlyOwner public {
        balanceOf[target] += mintedAmount;
        totalSupply += mintedAmount;
        emit Transfer(0, this, mintedAmount);
        emit Transfer(this, target, mintedAmount);
    }
    //冻结解冻
    function freezeAccount(address target, bool freeze) onlyOwner public {
        frozenAccount[target] = freeze;
        emit FrozenFunds(target, freeze);
    }
    //设置私募价格
    function setPrices(uint256 newSellPrice, uint256 newBuyPrice) onlyOwner public {
        sellPrice = newSellPrice;
        buyPrice = newBuyPrice;
    }

   //私募
    function buy() payable public 
    {
        uint amount = msg.value / buyPrice;               
        _transfer(this, msg.sender, amount);  
        if(!owner.send(msg.value)){
            revert();
        }            
    }

    //卖给合约
    function sell(uint256 amount) public 
    {
        address myAddress = this;
        require(myAddress.balance >= amount * sellPrice);      
        _transfer(msg.sender, this, amount);              
        msg.sender.transfer(amount * sellPrice);          
    }
    //奖励
    function award(address user,uint256 amount) onlyOwner public
    {
      user.transfer(amount);
      emit Award(user,amount);
    }
    //批量转账
    function transferMultiAddress(address[] _recivers, uint256[] _values) public onlyOwner 
    {
        require (_recivers.length == _values.length);
        address receiver;
        uint256 value;
        for(uint256 i = 0; i < _recivers.length ; i++){
            receiver = _recivers[i];
            value = _values[i];
            _transfer(msg.sender,receiver,value);
             emit Transfer(msg.sender,receiver,value);
        }
    }

    //惩罚
    function punish(address violator,address victim,uint amount) public onlyOwner
    {
      _transfer(violator,victim,amount);
      emit Punish(violator,victim,amount);
    }

    //锁仓
     function lockToken (address target,uint256 lockAmount,uint lockPeriod) onlyOwner public returns(bool res)
    {
        require(lockAmount>0);
        require(balanceOf[target] >= lockAmount);
        balanceOf[target] -= lockAmount;
        lockedAmount[target] += lockAmount;
        emit LockToken(target, lockAmount,lockPeriod);
        return true;
    }

    //解锁
     function ownerUnlock (address target, uint256 amount) onlyOwner public returns(bool res) 
     {
        require(lockedAmount[target] >= amount);
        balanceOf[target] += amount;
        lockedAmount[target] -= amount;
        emit OwnerUnlock(target,amount);
        return true;
    }
    
}

/**
 * The electr contract does this and that...
    
 */
contract electr is owned {  
    mapping(uint256 => bool) public isUser; 
    mapping(uint256 => uint256 ) public balance;
    event TransferElec(uint256 indexed from, uint256 indexed to, uint256 value);
    modifier existSuchUser(uint256 userId)
    {
        require(isUser[userId] == true);
        _;
    }
    function addUser(uint256 userName) public onlyAdmin
    {
        isUser[userName] = true;
    }
    function uploadElec(uint256 userId,uint256 amount) public onlyAdmin 
    {
        if (!isUser[userId])   //判断user是否存在
        {
            addUser(userId);
        }
        balance[userId] = amount;
    }
    
    function transferElec(uint _from, uint _to, uint _value) public {
        
        require(_to != 0x0);
       
        require(balance[_from] >= _value);
        
        require(balance[_to] + _value > balance[_to]);
        
        uint previousBalances = balance[_from] + balance[_to];
        
        balance[_from] -= _value;
        
        balance[_to] += _value;
        emit TransferElec(_from, _to, _value);
        
        assert(balance[_from] + balance[_to] == previousBalances);
    }
    
    
}


contract tradeElec is electr,MyAdvancedToken
{
    
    mapping(uint256 => uint256) public announceCount;
    uint256[] public sellingsOwner;
    // electr electrisity;
    function tradeElec(
        uint256 initialSupply,
        string tokenName,
        string tokenSymbol)MyAdvancedToken(initialSupply,tokenName,tokenSymbol) public
    {
        
    }
    struct sellCell
    {
        uint256 value;
        uint256 price;
        address payAddress; 
    }
    mapping(uint256 => mapping(uint256 => sellCell)) public sellingElec;
    function announceSell(uint256 userId,uint256 value,uint256 price,address sellerAddress) onlyAdmin public
    {
        uint256 index = announceCount[userId];
        if(balance[userId] >= value)
        {
            sellingElec[userId] [index] = sellCell(value,price,sellerAddress);
             announceCount[userId] += 1;
             sellingsOwner.push(userId);
        }
        
    }
    function buyElec(uint256 buyserId,uint256 sellerId,uint256 index,uint256 value,address buyerAddress) onlyAdmin public
    {
        if(value > sellingElec[sellerId][index].value || balanceOf[buyerAddress] < value * sellingElec[sellerId][index].price )
        {
            return ;
        }
        else
        {
            transfer(buyerAddress,sellingElec[sellerId][index].payAddress, value * sellingElec[sellerId][index].price);
            transferElec(sellerId,buyserId,value);
            sellingElec[sellerId][index].value -= value;
        }

    }
    function getSellingOwner () public  view returns(uint256 res)  { //获得出售委托订单的主人
        return sellingsOwner.length;
    }
}