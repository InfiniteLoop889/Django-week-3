program VarTypeDisplay;

type
  TVarType = (vtInteger, vtReal, vtString, vtBoolean);

function GetVarType(value: Integer): TVarType; overload;
begin
  Result := vtInteger;
end;

function GetVarType(value: Real): TVarType; overload;
begin
  Result := vtReal;
end;

function GetVarType(value: String): TVarType; overload;
begin
  Result := vtString;
end;

function GetVarType(value: Boolean): TVarType; overload;
begin
  Result := vtBoolean;
end;

function VarTypeToString(varType: TVarType): String;
begin
  case varType of
    vtInteger: Result := 'Integer';
    vtReal: Result := 'Real';
    vtString: Result := 'String';
    vtBoolean: Result := 'Boolean';
  else
    Result := 'Unknown';
  end;
end;

var
  intVar: Integer;
  realVar: Real;
  strVar: String;
  boolVar: Boolean;
begin
  intVar := 42;
  realVar := 3.14;
  strVar := 'Hello, world!';
  boolVar := True;

  WriteLn('intVar is of type: ', VarTypeToString(GetVarType(intVar)));
  WriteLn('realVar is of type: ', VarTypeToString(GetVarType(realVar)));
  WriteLn('strVar is of type: ', VarTypeToString(GetVarType(strVar)));
  WriteLn('boolVar is of type: ', VarTypeToString(GetVarType(boolVar)));
end.
