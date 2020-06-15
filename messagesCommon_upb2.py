from uprotobuf import *


Failuretype=enum(
    Failure_UnexpectedMessage=1,
    Failure_ButtonExpected=2,
    Failure_DataError=3,
    Failure_ActionCancelled=4,
    Failure_PinExpected=5,
    Failure_PinCancelled=6,
    Failure_PinInvalid=7,
    Failure_InvalidSignature=8,
    Failure_ProcessError=9,
    Failure_NotEnoughFunds=10,
    Failure_NotInitialized=11,
    Failure_PinMismatch=12,
    Failure_FirmwareError=99,
)

Buttonrequesttype=enum(
    ButtonRequest_Other=1,
    ButtonRequest_FeeOverThreshold=2,
    ButtonRequest_ConfirmOutput=3,
    ButtonRequest_ResetDevice=4,
    ButtonRequest_ConfirmWord=5,
    ButtonRequest_WipeDevice=6,
    ButtonRequest_ProtectCall=7,
    ButtonRequest_SignTx=8,
    ButtonRequest_FirmwareCheck=9,
    ButtonRequest_Address=10,
    ButtonRequest_PublicKey=11,
    ButtonRequest_MnemonicWordCount=12,
    ButtonRequest_MnemonicInput=13,
    ButtonRequest_PassphraseType=14,
    ButtonRequest_UnknownDerivationPath=15,
    ButtonRequest_RecoveryHomepage=16,
    ButtonRequest_Success=17,
    ButtonRequest_Warning=18,
)

Pinmatrixrequesttype=enum(
    PinMatrixRequestType_Current=1,
    PinMatrixRequestType_NewFirst=2,
    PinMatrixRequestType_NewSecond=3,
)

class SuccessMessage(Message):
    _proto_fields=[
        dict(name='message', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Optional, id=1),
    ]

class FailureMessage(Message):
    _proto_fields=[
        dict(name='code', type=WireType.Varint, subType=VarintSubType.Enum, fieldType=FieldType.Optional, id=1, enum=Failuretype),
        dict(name='message', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Optional, id=2),
    ]

class ButtonrequestMessage(Message):
    _proto_fields=[
        dict(name='code', type=WireType.Varint, subType=VarintSubType.Enum, fieldType=FieldType.Optional, id=1, enum=Buttonrequesttype),
    ]

class ButtonackMessage(Message):
    _proto_fields=[
    ]

class PinmatrixrequestMessage(Message):
    _proto_fields=[
        dict(name='type', type=WireType.Varint, subType=VarintSubType.Enum, fieldType=FieldType.Optional, id=1, enum=Pinmatrixrequesttype),
    ]

class PinmatrixackMessage(Message):
    _proto_fields=[
        dict(name='pin', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Required, id=1),
    ]

class PassphraserequestMessage(Message):
    _proto_fields=[
        dict(name='on_device', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=1),
    ]

class PassphraseackMessage(Message):
    _proto_fields=[
        dict(name='passphrase', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Optional, id=1),
        dict(name='state', type=WireType.Length, subType=LengthSubType.Bytes, fieldType=FieldType.Optional, id=2),
    ]

class PassphrasestaterequestMessage(Message):
    _proto_fields=[
        dict(name='state', type=WireType.Length, subType=LengthSubType.Bytes, fieldType=FieldType.Optional, id=1),
    ]

class PassphrasestateackMessage(Message):
    _proto_fields=[
    ]

class HdnodetypeMessage(Message):
    _proto_fields=[
        dict(name='depth', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Required, id=1),
        dict(name='fingerprint', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Required, id=2),
        dict(name='child_num', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Required, id=3),
        dict(name='chain_code', type=WireType.Length, subType=LengthSubType.Bytes, fieldType=FieldType.Required, id=4),
        dict(name='private_key', type=WireType.Length, subType=LengthSubType.Bytes, fieldType=FieldType.Optional, id=5),
        dict(name='public_key', type=WireType.Length, subType=LengthSubType.Bytes, fieldType=FieldType.Optional, id=6),
    ]
