from enum import Enum
from pydantic import Field, field_serializer
from typing import Optional
from models.base import BaseModel


class RecordingChannelsEnum(str, Enum):
    """The enum used to represent the recording channels."""
    mono = "mono"
    dual = "dual"


class RecordingTrimEnum(str, Enum):
    """The enum used to represent the recording trim option."""
    trim_silence = "trim-silence"
    do_not_trim = "do-not-trim"


class RecordingTrackEnum(str, Enum):
    """The enum used to represent the recording track option."""
    inbound = "inbound"
    outbound = "outbound"
    both = "both"


class MachineDetectionEnum(str, Enum):
    """The enum used to represent the machine detection."""
    enable = "Enable"
    detect_message_end = "DetectMessageEnd"


class VoiceMessage(BaseModel):
    """Provides a representation of a Twilio voice message."""

    from_: Optional[str] = Field(
        description="The phone number, SIP address, Client identifier or SIM SID that made this call.",
        alias="from",
        default=None,
    )
    """The phone number, SIP address, Client identifier or SIM SID that made this call."""

    to_: str = Field(
        description="The phone number, SIP address, Client identifier or SIM SID that received this call.",
        alias="to",
    )
    """The phone number, SIP address, Client identifier or SIM SID that received this call."""

    send_digits: Optional[str] = Field(
        description="The string of keys to dial after connecting to the number, with a maximum length of 32 digits.",
        alias="sendDigits",
        default=None,
    )
    """The string of keys to dial after connecting to the number, with a maximum length of 32 digits."""

    timeout: int = Field(
        description="The integer number of seconds that we should allow the phone to ring before assuming there is no answer.",
        default=60,
        ge=1,
        le=600,
    )
    """The integer number of seconds that we should allow the phone to ring before assuming there is no answer."""

    time_limit: Optional[int] = Field(
        description="The maximum duration of the call in seconds.",
        alias="timeLimit",
        default=None,
    )
    """The maximum duration of the call in seconds."""

    record: bool = Field(
        description="Whether to record the call.",
        default=False,
    )
    """Whether to record the call."""

    recording_channels: RecordingChannelsEnum = Field(
        description="The number of channels in the final recording.",
        alias="recordingChannels",
        default=RecordingChannelsEnum.mono,
    )
    """The number of channels in the final recording."""

    recording_track: RecordingTrackEnum = Field(
        description="The audio track to record for the call.",
        alias="recordingTrack",
        default=RecordingTrackEnum.both,
    )
    """The audio track to record for the call."""

    trim: RecordingTrimEnum = Field(
        description="Whether to trim any leading and trailing silence from the recording.",
        default=RecordingTrimEnum.trim_silence,
    )
    """Whether to trim any leading and trailing silence from the recording."""

    sip_auth_username: Optional[str] = Field(
        description="The username used to authenticate the caller making a SIP call.",
        alias="sipAuthUsername",
        default=None,
    )
    """The username used to authenticate the caller making a SIP call."""

    sip_auth_password: Optional[str] = Field(
        description="The password required to authenticate the user account specified in sip_auth_username.",
        alias="sipAuthPassword",
        default=None,
    )
    """The password required to authenticate the user account specified in sip_auth_username."""

    machine_detection: Optional[MachineDetectionEnum] = Field(
        description="Whether to detect if a human, answering machine, or fax has picked up the call.",
        alias="machineDetection",
        default=None,
    )
    """Whether to detect if a human, answering machine, or fax has picked up the call."""

    machine_detection_timeout: int = Field(
        description="The number of seconds that we should attempt to detect an answering machine before timing out and sending a voice request with AnsweredBy of unknown.",
        alias="machineDetectionTimeout",
        default=30,
        ge=1,
        le=60,
    )
    """The number of seconds that we should attempt to detect an answering machine before timing out and sending a voice request with AnsweredBy of unknown."""

    machine_detection_speech_threshold: int = Field(
        description="The number of milliseconds that is used as the measuring stick for the length of the speech activity, where durations lower than this value will be interpreted as a human and longer than this value as a machine.",
        alias="machineDetectionSpeechThreshold",
        default=2400,
        ge=1000,
        le=6000,
    )
    """The number of milliseconds that is used as the measuring stick for the length of the speech activity, where durations lower than this value will be interpreted as a human and longer than this value as a machine."""

    machine_detection_speech_end_threshold: int = Field(
        description="The number of milliseconds of silence after speech activity at which point the speech activity is considered complete.",
        alias="machineDetectionSpeechEndThreshold",
        default=1200,
        ge=500,
        le=5000,
    )
    """The number of milliseconds of silence after speech activity at which point the speech activity is considered complete."""

    machine_detection_silence_timeout: int = Field(
        description="The number of milliseconds of initial silence after which an unknown AnsweredBy result will be returned.",
        alias="machineDetectionSilenceTimeout",
        default=5000,
        ge=2000,
        le=10000,
    )
    """The number of milliseconds of initial silence after which an unknown AnsweredBy result will be returned."""

    async_amd: bool = Field(
        description="Select whether to perform answering machine detection in the background.",
        alias="asyncAmd",
        default=False,
    )
    """Select whether to perform answering machine detection in the background."""

    caller_id: Optional[str] = Field(
        description="The phone number, SIP address, or Client identifier that made this call.",
        alias="callerId",
        default=None,
    )
    """The phone number, SIP address, or Client identifier that made this call."""

    byoc: Optional[str] = Field(
        description="The SID of a BYOC (Bring Your Own Carrier) trunk to route this call with.",
        default=None,
        pattern="^BY[0-9a-fA-F]{32}$",
    )
    """The SID of a BYOC (Bring Your Own Carrier) trunk to route this call with."""

    call_reason: Optional[str] = Field(
        description="The Reason for the outgoing call.",
        alias="callReason",
        default=None,
    )
    """The Reason for the outgoing call."""

    @field_serializer('async_amd', mode='json')
    def serialize_async_amd(self, async_amd: bool, _info) -> str:
        return str(async_amd).lower()
