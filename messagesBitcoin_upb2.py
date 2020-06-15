from uprotobuf import *


Inputscripttype=enum(
    SPENDADDRESS=0,
    SPENDMULTISIG=1,
    EXTERNAL=2,
    SPENDWITNESS=3,
    SPENDP2SHWITNESS=4,
)

Requesttype=enum(
    TXINPUT=0,
    TXOUTPUT=1,
    TXMETA=2,
    TXFINISHED=3,
    TXEXTRADATA=4,
)

class MultisigredeemscripttypeMessage(Message):
    _proto_fields=[
        dict(name='pubkeys', type=WireType.Length, subType=LengthSubType.Message, fieldType=FieldType.Repeated, id=1),
        dict(name='signatures', type=WireType.Length, subType=LengthSubType.Bytes, fieldType=FieldType.Repeated, id=2),
        dict(name='m', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Optional, id=3),
        dict(name='nodes', type=WireType.Length, subType=LengthSubType.Message, fieldType=FieldType.Repeated, id=4),
        dict(name='address_n', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Repeated, id=5),
    ]

class GetpublickeyMessage(Message):
    _proto_fields=[
        dict(name='address_n', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Repeated, id=1),
        dict(name='ecdsa_curve_name', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Optional, id=2),
        dict(name='show_display', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=3),
        dict(name='coin_name', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Optional, id=4),
        dict(name='script_type', type=WireType.Varint, subType=VarintSubType.Enum, fieldType=FieldType.Optional, id=5, enum=Inputscripttype),
    ]

class PublickeyMessage(Message):
    _proto_fields=[
        dict(name='node', type=WireType.Length, subType=LengthSubType.Message, fieldType=FieldType.Optional, id=1),
        dict(name='xpub', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Optional, id=2),
    ]

class GetaddressMessage(Message):
    _proto_fields=[
        dict(name='address_n', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Repeated, id=1),
        dict(name='coin_name', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Optional, id=2),
        dict(name='show_display', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=3),
        dict(name='multisig', type=WireType.Length, subType=LengthSubType.Message, fieldType=FieldType.Optional, id=4),
        dict(name='script_type', type=WireType.Varint, subType=VarintSubType.Enum, fieldType=FieldType.Optional, id=5, enum=Inputscripttype),
    ]

class AddressMessage(Message):
    _proto_fields=[
        dict(name='address', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Required, id=1),
    ]

class SignmessageMessage(Message):
    _proto_fields=[
        dict(name='address_n', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Repeated, id=1),
        dict(name='message', type=WireType.Length, subType=LengthSubType.Bytes, fieldType=FieldType.Required, id=2),
        dict(name='coin_name', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Optional, id=3),
        dict(name='script_type', type=WireType.Varint, subType=VarintSubType.Enum, fieldType=FieldType.Optional, id=4, enum=Inputscripttype),
    ]

class MessagesignatureMessage(Message):
    _proto_fields=[
        dict(name='address', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Optional, id=1),
        dict(name='signature', type=WireType.Length, subType=LengthSubType.Bytes, fieldType=FieldType.Optional, id=2),
    ]

class VerifymessageMessage(Message):
    _proto_fields=[
        dict(name='address', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Optional, id=1),
        dict(name='signature', type=WireType.Length, subType=LengthSubType.Bytes, fieldType=FieldType.Optional, id=2),
        dict(name='message', type=WireType.Length, subType=LengthSubType.Bytes, fieldType=FieldType.Optional, id=3),
        dict(name='coin_name', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Optional, id=4),
    ]

class SigntxMessage(Message):
    _proto_fields=[
        dict(name='outputs_count', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Required, id=1),
        dict(name='inputs_count', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Required, id=2),
        dict(name='coin_name', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Optional, id=3),
        dict(name='version', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Optional, id=4),
        dict(name='lock_time', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Optional, id=5),
        dict(name='expiry', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Optional, id=6),
        dict(name='overwintered', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=7),
        dict(name='version_group_id', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Optional, id=8),
        dict(name='timestamp', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Optional, id=9),
        dict(name='branch_id', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Optional, id=10),
    ]

class TxrequestMessage(Message):
    _proto_fields=[
        dict(name='request_type', type=WireType.Varint, subType=VarintSubType.Enum, fieldType=FieldType.Optional, id=1, enum=Requesttype),
        dict(name='details', type=WireType.Length, subType=LengthSubType.Message, fieldType=FieldType.Optional, id=2),
        dict(name='serialized', type=WireType.Length, subType=LengthSubType.Message, fieldType=FieldType.Optional, id=3),
    ]

class TxackMessage(Message):
    _proto_fields=[
        dict(name='tx', type=WireType.Length, subType=LengthSubType.Message, fieldType=FieldType.Optional, id=1),
    ]

class PreparevaultMessage(Message):
    _proto_fields=[
        dict(name='signThis', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Required, id=1),
    ]

class PreparevaultresponseMessage(Message):
    _proto_fields=[
        dict(name='address', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Required, id=1),
        dict(name='redeemScript', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Required, id=2),
        dict(name='sig', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Required, id=3),
    ]

class FinalizevaultMessage(Message):
    _proto_fields=[
        dict(name='hex', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Required, id=1),
    ]

class FinalizevaultresponseMessage(Message):
    _proto_fields=[
        dict(name='isDeleted', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Required, id=1),
        dict(name='txid', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Required, id=2),
    ]

class UnvaultrequestMessage(Message):
    _proto_fields=[
        dict(name='txid', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Required, id=1),
    ]

class UnvaultresponseMessage(Message):
    _proto_fields=[
        dict(name='hex', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Required, id=1),
    ]

class ChecktotalbalanceMessage(Message):
    _proto_fields=[
    ]

class TotalbalanceMessage(Message):
    _proto_fields=[
        dict(name='balance', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Required, id=1),
    ]

class CheckvaultbalanceMessage(Message):
    _proto_fields=[
    ]

class VaultbalanceMessage(Message):
    _proto_fields=[
        dict(name='balance', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Required, id=1),
    ]

class CheckunvaultbalanceMessage(Message):
    _proto_fields=[
    ]

class UnvaultbalanceMessage(Message):
    _proto_fields=[
        dict(name='balance', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Required, id=1),
    ]

class Syncp2tstsMessage(Message):
    _proto_fields=[
    ]

class SyncresMessage(Message):
    _proto_fields=[
    ]
