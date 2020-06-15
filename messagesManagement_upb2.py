from uprotobuf import *


Backuptype=enum(
    Bip39=0,
    Slip39_Basic=1,
    Slip39_Advanced=2,
)

Capability=enum(
    Capability_Bitcoin=1,
    Capability_Bitcoin_like=2,
    Capability_Binance=3,
    Capability_Cardano=4,
    Capability_Crypto=5,
    Capability_EOS=6,
    Capability_Ethereum=7,
    Capability_Lisk=8,
    Capability_Monero=9,
    Capability_NEM=10,
    Capability_Ripple=11,
    Capability_Stellar=12,
    Capability_Tezos=13,
    Capability_U2F=14,
    Capability_Shamir=15,
    Capability_ShamirGroups=16,
)

Passphrasesourcetype=enum(
    ASK=0,
    DEVICE=1,
    HOST=2,
)

Sdprotectoperationtype=enum(
    DISABLE=0,
    ENABLE=1,
    REFRESH=2,
)

Recoverydevicetype=enum(
    RecoveryDeviceType_ScrambledWords=0,
    RecoveryDeviceType_Matrix=1,
)

Wordrequesttype=enum(
    WordRequestType_Plain=0,
    WordRequestType_Matrix9=1,
    WordRequestType_Matrix6=2,
)

class InitializeMessage(Message):
    _proto_fields=[
        dict(name='state', type=WireType.Length, subType=LengthSubType.Bytes, fieldType=FieldType.Optional, id=1),
        dict(name='skip_passphrase', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=2),
    ]

class GetfeaturesMessage(Message):
    _proto_fields=[
    ]

class FeaturesMessage(Message):
    _proto_fields=[
        dict(name='vendor', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Optional, id=1),
        dict(name='major_version', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Optional, id=2),
        dict(name='minor_version', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Optional, id=3),
        dict(name='patch_version', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Optional, id=4),
        dict(name='bootloader_mode', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=5),
        dict(name='device_id', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Optional, id=6),
        dict(name='pin_protection', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=7),
        dict(name='passphrase_protection', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=8),
        dict(name='language', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Optional, id=9),
        dict(name='label', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Optional, id=10),
        dict(name='initialized', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=12),
        dict(name='revision', type=WireType.Length, subType=LengthSubType.Bytes, fieldType=FieldType.Optional, id=13),
        dict(name='bootloader_hash', type=WireType.Length, subType=LengthSubType.Bytes, fieldType=FieldType.Optional, id=14),
        dict(name='imported', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=15),
        dict(name='pin_cached', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=16),
        dict(name='passphrase_cached', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=17),
        dict(name='firmware_present', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=18),
        dict(name='needs_backup', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=19),
        dict(name='flags', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Optional, id=20),
        dict(name='model', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Optional, id=21),
        dict(name='fw_major', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Optional, id=22),
        dict(name='fw_minor', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Optional, id=23),
        dict(name='fw_patch', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Optional, id=24),
        dict(name='fw_vendor', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Optional, id=25),
        dict(name='fw_vendor_keys', type=WireType.Length, subType=LengthSubType.Bytes, fieldType=FieldType.Optional, id=26),
        dict(name='unfinished_backup', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=27),
        dict(name='no_backup', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=28),
        dict(name='recovery_mode', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=29),
        dict(name='capabilities', type=WireType.Varint, subType=VarintSubType.Enum, fieldType=FieldType.Repeated, id=30, enum=Capability),
        dict(name='backup_type', type=WireType.Varint, subType=VarintSubType.Enum, fieldType=FieldType.Optional, id=31, enum=Backuptype),
        dict(name='sd_card_present', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=32),
        dict(name='sd_protection', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=33),
        dict(name='wipe_code_protection', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=34),
    ]

class ClearsessionMessage(Message):
    _proto_fields=[
    ]

class ApplysettingsMessage(Message):
    _proto_fields=[
        dict(name='language', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Optional, id=1),
        dict(name='label', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Optional, id=2),
        dict(name='use_passphrase', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=3),
        dict(name='homescreen', type=WireType.Length, subType=LengthSubType.Bytes, fieldType=FieldType.Optional, id=4),
        dict(name='passphrase_source', type=WireType.Varint, subType=VarintSubType.Enum, fieldType=FieldType.Optional, id=5, enum=Passphrasesourcetype),
        dict(name='auto_lock_delay_ms', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Optional, id=6),
        dict(name='display_rotation', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Optional, id=7),
    ]

class ApplyflagsMessage(Message):
    _proto_fields=[
        dict(name='flags', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Optional, id=1),
    ]

class ChangepinMessage(Message):
    _proto_fields=[
        dict(name='remove', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=1),
    ]

class ChangewipecodeMessage(Message):
    _proto_fields=[
        dict(name='remove', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=1),
    ]

class SdprotectMessage(Message):
    _proto_fields=[
        dict(name='operation', type=WireType.Varint, subType=VarintSubType.Enum, fieldType=FieldType.Optional, id=1, enum=Sdprotectoperationtype),
    ]

class PingMessage(Message):
    _proto_fields=[
        dict(name='message', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Optional, id=1),
        dict(name='button_protection', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=2),
        dict(name='pin_protection', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=3),
        dict(name='passphrase_protection', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=4),
    ]

class CancelMessage(Message):
    _proto_fields=[
    ]

class GetentropyMessage(Message):
    _proto_fields=[
        dict(name='size', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Required, id=1),
    ]

class EntropyMessage(Message):
    _proto_fields=[
        dict(name='entropy', type=WireType.Length, subType=LengthSubType.Bytes, fieldType=FieldType.Required, id=1),
    ]

class WipedeviceMessage(Message):
    _proto_fields=[
    ]

class LoaddeviceMessage(Message):
    _proto_fields=[
        dict(name='mnemonics', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Repeated, id=1),
        dict(name='pin', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Optional, id=3),
        dict(name='passphrase_protection', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=4),
        dict(name='language', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Optional, id=5),
        dict(name='label', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Optional, id=6),
        dict(name='skip_checksum', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=7),
        dict(name='u2f_counter', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Optional, id=8),
        dict(name='needs_backup', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=9),
        dict(name='no_backup', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=10),
    ]

class ResetdeviceMessage(Message):
    _proto_fields=[
        dict(name='display_random', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=1),
        dict(name='strength', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Optional, id=2),
        dict(name='passphrase_protection', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=3),
        dict(name='pin_protection', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=4),
        dict(name='language', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Optional, id=5),
        dict(name='label', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Optional, id=6),
        dict(name='u2f_counter', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Optional, id=7),
        dict(name='skip_backup', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=8),
        dict(name='no_backup', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=9),
        dict(name='backup_type', type=WireType.Varint, subType=VarintSubType.Enum, fieldType=FieldType.Optional, id=10, enum=Backuptype),
    ]

class BackupdeviceMessage(Message):
    _proto_fields=[
    ]

class EntropyrequestMessage(Message):
    _proto_fields=[
    ]

class EntropyackMessage(Message):
    _proto_fields=[
        dict(name='entropy', type=WireType.Length, subType=LengthSubType.Bytes, fieldType=FieldType.Optional, id=1),
    ]

class RecoverydeviceMessage(Message):
    _proto_fields=[
        dict(name='word_count', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Optional, id=1),
        dict(name='passphrase_protection', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=2),
        dict(name='pin_protection', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=3),
        dict(name='language', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Optional, id=4),
        dict(name='label', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Optional, id=5),
        dict(name='enforce_wordlist', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=6),
        dict(name='type', type=WireType.Varint, subType=VarintSubType.Enum, fieldType=FieldType.Optional, id=8, enum=Recoverydevicetype),
        dict(name='u2f_counter', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Optional, id=9),
        dict(name='dry_run', type=WireType.Varint, subType=VarintSubType.Bool, fieldType=FieldType.Optional, id=10),
    ]

class WordrequestMessage(Message):
    _proto_fields=[
        dict(name='type', type=WireType.Varint, subType=VarintSubType.Enum, fieldType=FieldType.Optional, id=1, enum=Wordrequesttype),
    ]

class WordackMessage(Message):
    _proto_fields=[
        dict(name='word', type=WireType.Length, subType=LengthSubType.String, fieldType=FieldType.Required, id=1),
    ]

class Setu2fcounterMessage(Message):
    _proto_fields=[
        dict(name='u2f_counter', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Optional, id=1),
    ]

class Getnextu2fcounterMessage(Message):
    _proto_fields=[
    ]

class Nextu2fcounterMessage(Message):
    _proto_fields=[
        dict(name='u2f_counter', type=WireType.Varint, subType=VarintSubType.UInt32, fieldType=FieldType.Optional, id=1),
    ]

class DevboardinitializeMessage(Message):
    _proto_fields=[
    ]

class DevboardinitializeresMessage(Message):
    _proto_fields=[
    ]
