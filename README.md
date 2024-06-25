# TS-Packet-Analyser
## Overview
TS-Packet-Analyser is a tool for analyzing MPEG-2 Transport Stream (TS) packets. This tool provides detailed insights into the structure and content of TS packets, including PAT, PMT, and other tables, making it useful for debugging and learning about MPEG-2 TS streams. This project was developed as part of an internship.

## Features
Analyzes MPEG-2 Transport Stream packets
Displays detailed information about Program Association Table (PAT) and Program Map Table (PMT)
User-friendly interface for visualizing TS packet contents using PyQt

## Screenshots

![Main Window](https://github.com/Soheilnader/TS-Packet-Analyser/blob/main/docs/images/MainWindow.png?raw=true )



## MPEG Transport Stream
MPEG-TS, or MPEG Transport Stream, is a standard digital container format used for transmitting and storing audio, video, and data. It is commonly used in broadcasting systems such as DVB (Digital Video Broadcasting), ATSC (Advanced Television Systems Committee), and IPTV (Internet Protocol Television).

### Key Features of MPEG-TS:
#### Packetized Data:

Fixed-size Packets: Each packet is typically 188 bytes in size. This standard size facilitates synchronization and error correction.
Packet Identification (PID): Each packet contains a Packet Identifier to differentiate between different types of data streams within the same transport stream, such as audio, video, and metadata.
#### Error Correction and Synchronization:

Error Detection: MPEG-TS includes mechanisms for detecting errors, such as the Cyclic Redundancy Check (CRC).
Synchronization: Packets include synchronization bytes that help in maintaining the correct sequence of data packets.
#### Multiplexing:

MPEG-TS can carry multiple programs simultaneously. Each program can consist of multiple streams of audio, video, and other data.
Program Specific Information (PSI): This includes metadata about the streams, such as the Program Association Table (PAT) and the Program Map Table (PMT), which help in demultiplexing the streams at the receiver end.
#### Real-time Transmission:

MPEG-TS is designed for real-time broadcasting and streaming, ensuring timely delivery of data packets with minimal latency.
Adaptive Bitrate Streaming: It supports varying bit rates to adjust to different network conditions, ensuring smooth streaming even with bandwidth fluctuations.
### Applications of MPEG-TS:
#### Broadcast Television:

Used in terrestrial, satellite, and cable broadcasting.
Ensures reliable transmission of high-quality video and audio signals over long distances.
#### IPTV and Streaming Services:

Employed in delivering live TV and on-demand content over the internet.
Supports adaptive streaming technologies like HLS (HTTP Live Streaming) and MPEG-DASH (Dynamic Adaptive Streaming over HTTP).
#### Video Surveillance:

Utilized in CCTV systems for transmitting video feeds from multiple cameras to a central monitoring station.
#### Media Storage and Distribution:

Used in media servers and storage devices for efficient storage and playback of multimedia content.
Ensures compatibility with various playback devices and software.
### Technical Components of MPEG-TS:
#### PAT (Program Association Table):

Contains a list of all programs in the transport stream and their corresponding PMT PIDs.
#### PMT (Program Map Table):

Provides information about the streams that make up each program, including their types and PIDs.
#### CAT (Conditional Access Table):

Contains information about conditional access systems used for encrypting the transport stream.
#### ES (Elementary Stream):

The raw data stream (audio, video, or other) contained within the transport stream packets.
#### PES (Packetized Elementary Stream):

Elementary streams are packetized into PES packets, which are then segmented into fixed-size transport stream packets.
