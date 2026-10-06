import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="PeerShield - P2P Computing",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ PeerShield")
st.caption("FI1922 • Peer-to-Peer Computing • Secure Real-Time P2P Collaboration")

st.info(
    "Open this application in two browsers/devices. "
    "Exchange the Peer ID shown below and establish a direct P2P connection. "
    "Chat, share files, collaborate, and test the security controls."
)

html = r"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">

<script src="https://unpkg.com/peerjs@1.5.4/dist/peerjs.min.js"></script>

<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 16px;
    font-family: Inter, Arial, sans-serif;
    background: #0b1220;
    color: #e5e7eb;
}

.container {
    max-width: 1100px;
    margin: auto;
}

.hero {
    background: linear-gradient(135deg, #111827, #172554);
    border: 1px solid #26355f;
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 16px;
}

.hero h1 {
    margin: 0 0 8px 0;
    font-size: 28px;
}

.hero p {
    color: #a5b4fc;
    margin: 4px 0;
}

.grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin-bottom: 16px;
}

.card {
    background: #111827;
    border: 1px solid #263244;
    border-radius: 14px;
    padding: 16px;
}

.card h3 {
    margin-top: 0;
}

.metric {
    font-size: 27px;
    font-weight: bold;
    color: #60a5fa;
}

.label {
    font-size: 12px;
    color: #94a3b8;
    text-transform: uppercase;
}

input, textarea {
    width: 100%;
    background: #020617;
    border: 1px solid #334155;
    color: white;
    border-radius: 9px;
    padding: 10px;
    margin: 6px 0;
}

textarea {
    min-height: 180px;
    resize: vertical;
}

button {
    border: none;
    border-radius: 9px;
    padding: 10px 15px;
    margin: 4px 3px 4px 0;
    background: #2563eb;
    color: white;
    cursor: pointer;
    font-weight: 600;
}

button:hover {
    background: #1d4ed8;
}

button.secondary {
    background: #374151;
}

button.danger {
    background: #dc2626;
}

button.success {
    background: #059669;
}

button.warning {
    background: #d97706;
}

.tabs {
    display: flex;
    gap: 6px;
    margin-bottom: 12px;
    flex-wrap: wrap;
}

.tab {
    background: #1e293b;
}

.tab.active {
    background: #2563eb;
}

.panel {
    display: none;
}

.panel.active {
    display: block;
}

#chat {
    height: 310px;
    overflow-y: auto;
    background: #020617;
    border-radius: 10px;
    border: 1px solid #1e293b;
    padding: 12px;
}

.msg {
    margin-bottom: 10px;
    padding: 9px;
    border-radius: 8px;
    background: #172033;
}

.msg.me {
    background: #172554;
}

.msg.system {
    background: #172a1d;
    color: #86efac;
}

.msg small {
    color: #94a3b8;
}

.peer-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #020617;
    border: 1px solid #1e293b;
    padding: 10px;
    border-radius: 9px;
    margin: 6px 0;
}

.badge {
    padding: 4px 8px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: bold;
}

.green {
    background: #064e3b;
    color: #6ee7b7;
}

.red {
    background: #450a0a;
    color: #fca5a5;
}

.yellow {
    background: #451a03;
    color: #fcd34d;
}

.blue {
    background: #172554;
    color: #93c5fd;
}

.hash {
    font-family: monospace;
    word-break: break-all;
    color: #93c5fd;
    background: #020617;
    padding: 8px;
    border-radius: 7px;
    font-size: 11px;
}

.log {
    max-height: 220px;
    overflow-y: auto;
    font-family: monospace;
    font-size: 12px;
    background: #020617;
    padding: 10px;
    border-radius: 8px;
}

.log div {
    padding: 3px;
    border-bottom: 1px solid #111827;
}

.notice {
    padding: 12px;
    border-radius: 9px;
    background: #172033;
    border-left: 4px solid #3b82f6;
    margin: 8px 0;
}

.success-box {
    background: #052e1b;
    border: 1px solid #166534;
    color: #86efac;
    padding: 12px;
    border-radius: 9px;
}

.danger-box {
    background: #450a0a;
    border: 1px solid #991b1b;
    color: #fca5a5;
    padding: 12px;
    border-radius: 9px;
}

@media(max-width: 800px) {
    .grid {
        grid-template-columns: 1fr;
    }
}
</style>
</head>

<body>

<div class="container">

<div class="hero">
    <h1>🛡️ PeerShield Network</h1>
    <p>Secure P2P file sharing • real-time messaging • collaboration • reputation</p>
    <p id="status">Initializing peer...</p>
</div>

<div class="grid">

    <div class="card">
        <div class="label">My Peer ID</div>
        <div id="myPeerId" class="metric">...</div>
        <button onclick="copyPeerId()">Copy ID</button>
    </div>

    <div class="card">
        <div class="label">Connected Peers</div>
        <div id="peerCount" class="metric">0</div>
    </div>

    <div class="card">
        <div class="label">Trust Score</div>
        <div id="trustScore" class="metric">100</div>
    </div>

</div>

<div class="tabs">
    <button class="tab active" onclick="showTab('network', this)">🌐 Network</button>
    <button class="tab" onclick="showTab('chatTab', this)">💬 Chat</button>
    <button class="tab" onclick="showTab('files', this)">📁 Files</button>
    <button class="tab" onclick="showTab('collab', this)">📝 Collaboration</button>
    <button class="tab" onclick="showTab('security', this)">🛡️ Security</button>
    <button class="tab" onclick="showTab('stats', this)">📊 Analytics</button>
</div>

<div id="network" class="panel active">

    <div class="card">
        <h3>Connect to another peer</h3>

        <label>Your display name</label>
        <input id="displayName" placeholder="Example: Student-A" value="Student">

        <label>Remote Peer ID</label>
        <input id="remotePeer" placeholder="Paste the other peer's ID">

        <button class="success" onclick="connectToPeer()">🔗 Establish P2P Connection</button>

        <div id="connectionStatus" class="notice">
            Waiting for a peer connection...
        </div>
    </div>

    <div class="card">
        <h3>Connected Network</h3>
        <div id="peerList"></div>
    </div>

</div>

<div id="chatTab" class="panel">

    <div class="card">
        <h3>💬 P2P Instant Messaging</h3>

        <div id="chat"></div>

        <input id="chatInput"
               placeholder="Type a message..."
               onkeydown="if(event.key==='Enter') sendChat()">

        <button onclick="sendChat()">Send</button>
        <button class="secondary" onclick="sendPing()">📡 Ping Peer</button>
    </div>

</div>

<div id="files" class="panel">

    <div class="card">

        <h3>📁 Direct P2P File Sharing</h3>

        <div class="notice">
            Files are transferred through the peer connection. The application
            calculates SHA-256 before transmission and after reception.
        </div>

        <input type="file" id="fileInput">

        <label>
            <input type="checkbox" id="tamperTest" style="width:auto">
            Simulate malicious peer / tampered payload
        </label>

        <br>

        <button class="success" onclick="sendFile()">🚀 Send File Directly</button>

        <div id="fileResult"></div>

    </div>

    <div class="card">

        <h3>Received Files</h3>

        <div id="receivedFiles">
            No files received yet.
        </div>

    </div>

</div>

<div id="collab" class="panel">

    <div class="card">

        <h3>📝 P2P Collaborative Workspace</h3>

        <div class="notice">
            Type in the document. Changes are broadcast directly to connected peers.
        </div>

        <textarea id="sharedNote"
                  placeholder="Start writing a collaborative note..."
                  oninput="scheduleNoteSync()"></textarea>

        <button onclick="requestNote()">🔄 Request Latest Note</button>
        <button class="secondary" onclick="clearNote()">Clear</button>

    </div>

</div>

<div id="security" class="panel">

    <div class="grid">

        <div class="card">
            <h3>🔐 Transport</h3>
            <p>
                PeerShield uses WebRTC DataChannels through PeerJS.
                The browser handles the encrypted transport layer.
            </p>
            <span class="badge green">P2P ENCRYPTED CHANNEL</span>
        </div>

        <div class="card">
            <h3>🔎 Integrity</h3>
            <p>
                Every file gets a SHA-256 fingerprint.
            </p>
            <span class="badge blue">SHA-256</span>
        </div>

        <div class="card">
            <h3>🚨 Threat Control</h3>
            <p>
                Peers can be quarantined when suspicious behavior is detected.
            </p>
            <span class="badge red">QUARANTINE</span>
        </div>

    </div>

    <div class="card">

        <h3>Peer Trust Management</h3>

        <div id="securityPeers"></div>

        <br>

        <button class="warning" onclick="simulateAttack()">
            🧪 Simulate Suspicious Peer
        </button>

        <button class="danger" onclick="quarantineAll()">
            🚫 Quarantine All
        </button>

    </div>

</div>

<div id="stats" class="panel">

    <div class="grid">

        <div class="card">
            <div class="label">Messages Sent</div>
            <div id="sentMessages" class="metric">0</div>
        </div>

        <div class="card">
            <div class="label">Messages Received</div>
            <div id="receivedMessages" class="metric">0</div>
        </div>

        <div class="card">
            <div class="label">Files Sent</div>
            <div id="filesSent" class="metric">0</div>
        </div>

        <div class="card">
            <div class="label">Files Received</div>
            <div id="filesReceived" class="metric">0</div>
        </div>

        <div class="card">
            <div class="label">Bytes Sent</div>
            <div id="bytesSent" class="metric">0</div>
        </div>

        <div class="card">
            <div class="label">Bytes Received</div>
            <div id="bytesReceived" class="metric">0</div>
        </div>

    </div>

    <div class="card">
        <h3>Network Event Log</h3>
        <div id="eventLog" class="log"></div>
    </div>

</div>

</div>

<script>

let peer;
let connections = {};
let quarantined = new Set();

let stats = {
    messagesSent: 0,
    messagesReceived: 0,
    filesSent: 0,
    filesReceived: 0,
    bytesSent: 0,
    bytesReceived: 0
};

let reputation = {};
let incomingFiles = {};
let noteTimer = null;

function logEvent(message) {
    const log = document.getElementById("eventLog");
    const time = new Date().toLocaleTimeString();

    const row = document.createElement("div");
    row.textContent = "[" + time + "] " + message;

    log.prepend(row);
}

function setStatus(message) {
    document.getElementById("status").textContent = message;
}

function showTab(id, button) {

    document.querySelectorAll(".panel").forEach(
        p => p.classList.remove("active")
    );

    document.querySelectorAll(".tab").forEach(
        b => b.classList.remove("active")
    );

    document.getElementById(id).classList.add("active");

    if(button) {
        button.classList.add("active");
    }
}

function addChatMessage(sender, message, type="normal") {

    const chat = document.getElementById("chat");

    const div = document.createElement("div");
    div.className = "msg " + type;

    const title = document.createElement("b");
    title.textContent = sender;

    const small = document.createElement("small");
    small.textContent = " • " + new Date().toLocaleTimeString();

    const text = document.createElement("div");
    text.textContent = message;

    div.appendChild(title);
    div.appendChild(small);
    div.appendChild(text);

    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

function generateReputation(peerId) {

    if(!reputation[peerId]) {
        reputation[peerId] = {
            score: 50,
            sent: 0,
            received: 0,
            violations: 0
        };
    }

    return reputation[peerId];
}

function updateTrustScore() {

    let scores = Object.values(reputation);

    if(scores.length === 0) {
        document.getElementById("trustScore").textContent = "100";
        return;
    }

    let avg = scores.reduce((a,b) => a + b.score, 0) / scores.length;

    document.getElementById("trustScore").textContent =
        Math.max(0, Math.round(avg));
}

function changeReputation(peerId, amount, reason) {

    let r = generateReputation(peerId);

    r.score = Math.max(0, Math.min(100, r.score + amount));

    logEvent(
        "Reputation " +
        (amount >= 0 ? "+" : "") +
        amount +
        " for " +
        peerId +
        " (" +
        reason +
        ")"
    );

    if(r.score < 20) {
        quarantined.add(peerId);

        if(connections[peerId]) {
            connections[peerId].close();
        }

        logEvent("Peer " + peerId + " automatically quarantined.");
    }

    updateTrustScore();
    renderPeers();
}

function initPeer() {

    try {

        peer = new Peer({
            debug: 1
        });

        peer.on("open", function(id) {

            document.getElementById("myPeerId").textContent = id;

            setStatus("🟢 Online • Ready for P2P connections");

            logEvent("Peer initialized with ID " + id);

        });

        peer.on("connection", function(conn) {

            handleConnection(conn);

        });

        peer.on("error", function(error) {

            setStatus("⚠️ " + error.type);

            logEvent("Peer error: " + error.type);

        });

        peer.on("disconnected", function() {

            setStatus("🟡 Disconnected from signaling service");

        });

        peer.on("close", function() {

            setStatus("🔴 Peer closed");

        });

    } catch(error) {

        setStatus("Initialization failed");

        logEvent(error.message);

    }

}

function connectToPeer() {

    const remote = document.getElementById("remotePeer").value.trim();

    if(!remote) {
        alert("Enter a remote Peer ID.");
        return;
    }

    if(quarantined.has(remote)) {
        alert("This peer is quarantined.");
        return;
    }

    const conn = peer.connect(remote, {
        reliable: true,
        metadata: {
            name: document.getElementById("displayName").value || "Anonymous"
        }
    });

    handleConnection(conn);
}

function handleConnection(conn) {

    const peerId = conn.peer;

    if(quarantined.has(peerId)) {
        conn.close();
        return;
    }

    connections[peerId] = conn;

    generateReputation(peerId);

    conn.on("open", function() {

        document.getElementById("connectionStatus").innerHTML =
            "🟢 Connected directly to <b>" +
            peerId +
            "</b>";

        const myName =
            document.getElementById("displayName").value || "Anonymous";

        conn.send({
            type: "hello",
            name: myName
        });

        logEvent("Direct P2P connection established with " + peerId);

        renderPeers();
    });

    conn.on("data", function(data) {

        receiveData(conn, data);

    });

    conn.on("close", function() {

        delete connections[peerId];

        logEvent("Peer disconnected: " + peerId);

        renderPeers();

    });

    conn.on("error", function(error) {

        logEvent(
            "Connection error with " +
            peerId +
            ": " +
            error.message
        );

    });

    renderPeers();
}

function receiveData(conn, data) {

    const peerId = conn.peer;

    if(quarantined.has(peerId)) {
        return;
    }

    if(data instanceof ArrayBuffer ||
       data instanceof Uint8Array ||
       data instanceof Blob) {

        receiveFileChunk(peerId, data);

        return;
    }

    if(typeof data !== "object") {
        return;
    }

    switch(data.type) {

        case "hello":

            addChatMessage(
                data.name || peerId,
                "Peer connected successfully.",
                "system"
            );

            logEvent(
                data.name +
                " joined the P2P network."
            );

            break;

        case "chat":

            stats.messagesReceived++;

            document.getElementById("receivedMessages").textContent =
                stats.messagesReceived;

            addChatMessage(
                data.name || peerId,
                data.message
            );

            changeReputation(
                peerId,
                1,
                "valid message"
            );

            break;

        case "ping":

            conn.send({
                type: "pong",
                time: data.time
            });

            break;

        case "pong":

            const delay = Date.now() - data.time;

            addChatMessage(
                "NETWORK",
                "P2P latency: " + delay + " ms",
                "system"
            );

            break;

        case "file-meta":

            incomingFiles[data.transferId] = {
                peerId: peerId,
                name: data.name,
                size: data.size,
                type: data.fileType || "application/octet-stream",
                hash: data.hash,
                totalChunks: data.totalChunks,
                receivedChunks: 0,
                chunks: []
            };

            addChatMessage(
                "FILE",
                "Receiving " + data.name +
                " from " + peerId,
                "system"
            );

            logEvent(
                "Started receiving " +
                data.name +
                " from " +
                peerId
            );

            break;

        case "file-complete":

            break;

        case "note":

            document.getElementById("sharedNote").value =
                data.text;

            logEvent(
                "Collaborative document synchronized from " +
                peerId
            );

            changeReputation(
                peerId,
                1,
                "collaboration"
            );

            break;

        case "note-request":

            sendCurrentNote(conn);

            break;

        case "suspicious":

            changeReputation(
                peerId,
                -20,
                "suspicious behavior"
            );

            addChatMessage(
                "SECURITY",
                "Suspicious activity reported by " +
                peerId,
                "system"
            );

            break;
    }
}

function sendChat() {

    const input = document.getElementById("chatInput");
    const message = input.value.trim();

    if(!message) {
        return;
    }

    const name =
        document.getElementById("displayName").value ||
        "Anonymous";

    let sent = 0;

    Object.entries(connections).forEach(([id, conn]) => {

        if(
            conn.open &&
            !quarantined.has(id)
        ) {

            conn.send({
                type: "chat",
                name: name,
                message: message,
                timestamp: Date.now()
            });

            sent++;

            generateReputation(id).sent++;
            changeReputation(
                id,
                1,
                "sharing"
            );
        }

    });

    if(sent === 0) {

        addChatMessage(
            "SYSTEM",
            "No connected peer.",
            "system"
        );

        return;
    }

    stats.messagesSent += sent;

    document.getElementById("sentMessages").textContent =
        stats.messagesSent;

    addChatMessage(
        "Me",
        message,
        "me"
    );

    input.value = "";

}

function sendPing() {

    let sent = false;

    Object.values(connections).forEach(conn => {

        if(conn.open) {

            conn.send({
                type: "ping",
                time: Date.now()
            });

            sent = true;
        }

    });

    if(!sent) {
        addChatMessage(
            "SYSTEM",
            "No connected peer.",
            "system"
        );
    }
}

async function sha256(buffer) {

    const hashBuffer =
        await crypto.subtle.digest(
            "SHA-256",
            buffer
        );

    const hashArray =
        Array.from(new Uint8Array(hashBuffer));

    return hashArray
        .map(
            b => b.toString(16).padStart(2, "0")
        )
        .join("");
}

function formatBytes(bytes) {

    if(bytes < 1024)
        return bytes + " B";

    if(bytes < 1024 * 1024)
        return (bytes / 1024).toFixed(2) + " KB";

    return (bytes / (1024 * 1024)).toFixed(2) + " MB";
}

async function sendFile() {

    const input =
        document.getElementById("fileInput");

    const file = input.files[0];

    if(!file) {

        alert("Choose a file first.");

        return;
    }

    const peers =
        Object.entries(connections)
        .filter(
            ([id, conn]) =>
                conn.open &&
                !quarantined.has(id)
        );

    if(peers.length === 0) {

        alert("Connect to a peer first.");

        return;
    }

    const result =
        document.getElementById("fileResult");

    result.innerHTML =
        "<div class='notice'>Calculating SHA-256...</div>";

    const buffer =
        await file.arrayBuffer();

    const originalHash =
        await sha256(buffer);

    const chunkSize = 48 * 1024;

    const totalChunks =
        Math.ceil(buffer.byteLength / chunkSize);

    const transferId =
        Date.now().toString(36) +
        Math.random().toString(36).substring(2);

    const tamper =
        document.getElementById("tamperTest").checked;

    for(
        const [peerId, conn]
        of peers
    ) {

        conn.send({
            type: "file-meta",
            transferId: transferId + "-" + peerId,
            name: file.name,
            size: file.size,
            fileType: file.type,
            hash: originalHash,
            totalChunks: totalChunks
        });

        for(
            let i = 0;
            i < totalChunks;
            i++
        ) {

            let start =
                i * chunkSize;

            let end =
                Math.min(
                    start + chunkSize,
                    buffer.byteLength
                );

            let chunk =
                buffer.slice(
                    start,
                    end
                );

            if(
                tamper &&
                i === Math.floor(totalChunks / 2)
            ) {

                const corrupted =
                    new Uint8Array(chunk);

                if(corrupted.length > 0) {

                    corrupted[0] =
                        corrupted[0] ^ 255;
                }

                chunk = corrupted.buffer;

                logEvent(
                    "⚠️ Tamper simulation activated."
                );
            }

            conn.send(chunk);

            stats.bytesSent +=
                chunk.byteLength;

            await new Promise(
                resolve =>
                    setTimeout(resolve, 2)
            );
        }

        stats.filesSent++;

        generateReputation(peerId).sent++;

        changeReputation(
            peerId,
            3,
            "file sharing"
        );
    }

    document.getElementById("filesSent").textContent =
        stats.filesSent;

    document.getElementById("bytesSent").textContent =
        formatBytes(stats.bytesSent);

    result.innerHTML =
        "<div class='success-box'>" +
        "File transmitted. SHA-256: " +
        "<div class='hash'>" +
        originalHash +
        "</div></div>";

    logEvent(
        "File " +
        file.name +
        " sent to " +
        peers.length +
        " peer(s)."
    );
}

async function receiveFileChunk(peerId, data) {

    let candidates =
        Object.entries(incomingFiles)
        .filter(
            ([id, file]) =>
                file.peerId === peerId &&
                file.receivedChunks < file.totalChunks
        );

    if(candidates.length === 0) {
        return;
    }

    const transferId =
        candidates[candidates.length - 1][0];

    const file =
        incomingFiles[transferId];

    let arrayBuffer;

    if(data instanceof Blob) {

        arrayBuffer =
            await data.arrayBuffer();

    } else if(data instanceof Uint8Array) {

        arrayBuffer =
            data.buffer.slice(
                data.byteOffset,
                data.byteOffset + data.byteLength
            );

    } else {

        arrayBuffer = data;
    }

    file.chunks.push(arrayBuffer);

    file.receivedChunks++;

    stats.bytesReceived +=
        arrayBuffer.byteLength;

    if(
        file.receivedChunks >=
        file.totalChunks
    ) {

        const combined =
            new Blob(
                file.chunks,
                {
                    type: file.type
                }
            );

        const buffer =
            await combined.arrayBuffer();

        const receivedHash =
            await sha256(buffer);

        stats.filesReceived++;

        document.getElementById("filesReceived").textContent =
            stats.filesReceived;

        document.getElementById("bytesReceived").textContent =
            formatBytes(stats.bytesReceived);

        const verified =
            receivedHash === file.hash;

        const container =
            document.getElementById("receivedFiles");

        const box =
            document.createElement("div");

        box.className =
            verified
            ? "success-box"
            : "danger-box";

        const title =
            document.createElement("b");

        title.textContent =
            file.name;

        box.appendChild(title);

        const info =
            document.createElement("div");

        info.textContent =
            "Size: " +
            formatBytes(file.size);

        box.appendChild(info);

        const status =
            document.createElement("div");

        status.style.marginTop = "8px";

        status.textContent =
            verified
            ? "✅ SHA-256 VERIFIED — File integrity intact."
            : "🚨 INTEGRITY FAILURE — Possible tampering detected.";

        box.appendChild(status);

        const hash1 =
            document.createElement("div");

        hash1.className = "hash";

        hash1.textContent =
            "Expected: " + file.hash;

        box.appendChild(hash1);

        const hash2 =
            document.createElement("div");

        hash2.className = "hash";

        hash2.textContent =
            "Received: " + receivedHash;

        box.appendChild(hash2);

        if(verified) {

            const download =
                document.createElement("a");

            download.href =
                URL.createObjectURL(combined);

            download.download =
                file.name;

            download.textContent =
                "⬇️ Download Verified File";

            download.style.display =
                "inline-block";

            download.style.marginTop =
                "10px";

            download.style.color =
                "#93c5fd";

            box.appendChild(download);

            changeReputation(
                peerId,
                5,
                "verified file"
            );

        } else {

            changeReputation(
                peerId,
                -30,
                "file integrity failure"
            );

            quarantined.add(peerId);

            if(connections[peerId]) {
                connections[peerId].close();
            }

            logEvent(
                "🚨 Peer " +
                peerId +
                " quarantined because of integrity failure."
            );
        }

        container.prepend(box);

        logEvent(
            verified
            ? "SHA-256 verified for " + file.name
            : "🚨 SHA-256 mismatch for " + file.name
        );

        delete incomingFiles[transferId];
    }
}

function scheduleNoteSync() {

    clearTimeout(noteTimer);

    noteTimer =
        setTimeout(
            broadcastNote,
            400
        );
}

function broadcastNote() {

    const text =
        document.getElementById("sharedNote").value;

    Object.entries(connections).forEach(
        ([id, conn]) => {

            if(
                conn.open &&
                !quarantined.has(id)
            ) {

                conn.send({
                    type: "note",
                    text: text,
                    timestamp: Date.now()
                });

            }

        }
    );
}

function requestNote() {

    Object.values(connections).forEach(
        conn => {

            if(conn.open) {

                conn.send({
                    type: "note-request"
                });

            }

        }
    );

    logEvent("Requested latest collaborative document.");
}

function sendCurrentNote(conn) {

    conn.send({
        type: "note",
        text:
            document.getElementById("sharedNote").value,
        timestamp: Date.now()
    });
}

function clearNote() {

    document.getElementById("sharedNote").value = "";

    broadcastNote();
}

function simulateAttack() {

    const ids =
        Object.keys(connections);

    if(ids.length === 0) {

        alert(
            "Connect at least one peer before running the attack simulation."
        );

        return;
    }

    const target =
        ids[0];

    generateReputation(target);

    reputation[target].violations++;

    changeReputation(
        target,
        -20,
        "simulated suspicious activity"
    );

    if(connections[target]) {

        connections[target].send({
            type: "suspicious"
        });
    }

    addChatMessage(
        "SECURITY",
        "Suspicious behavior simulation executed against " +
        target,
        "system"
    );

    logEvent(
        "🧪 Security attack simulation executed."
    );
}

function quarantinePeer(id) {

    quarantined.add(id);

    if(connections[id]) {
        connections[id].close();
    }

    logEvent(
        "Peer " +
        id +
        " manually quarantined."
    );

    renderPeers();
}

function quarantineAll() {

    Object.keys(connections).forEach(
        id => quarantinePeer(id)
    );
}

function renderPeers() {

    const peerList =
        document.getElementById("peerList");

    const securityPeers =
        document.getElementById("securityPeers");

    peerList.innerHTML = "";
    securityPeers.innerHTML = "";

    const ids =
        Object.keys(connections);

    document.getElementById("peerCount").textContent =
        ids.filter(
            id => !quarantined.has(id)
        ).length;

    if(ids.length === 0) {

        peerList.innerHTML =
            "<div class='notice'>No peers connected.</div>";

        securityPeers.innerHTML =
            "<div class='notice'>No peer reputation records.</div>";

        updateTrustScore();

        return;
    }

    ids.forEach(id => {

        const r =
            generateReputation(id);

        const row =
            document.createElement("div");

        row.className = "peer-row";

        const left =
            document.createElement("div");

        const name =
            document.createElement("b");

        name.textContent =
            id;

        left.appendChild(name);

        const details =
            document.createElement("div");

        details.style.color =
            "#94a3b8";

        details.style.fontSize =
            "12px";

        details.textContent =
            "Sent: " +
            r.sent +
            " • Received: " +
            r.received +
            " • Violations: " +
            r.violations;

        left.appendChild(details);

        row.appendChild(left);

        const badge =
            document.createElement("span");

        if(quarantined.has(id)) {

            badge.className =
                "badge red";

            badge.textContent =
                "QUARANTINED";

        } else if(r.score >= 70) {

            badge.className =
                "badge green";

            badge.textContent =
                "TRUST " +
                r.score;

        } else if(r.score >= 40) {

            badge.className =
                "badge yellow";

            badge.textContent =
                "TRUST " +
                r.score;

        } else {

            badge.className =
                "badge red";

            badge.textContent =
                "LOW TRUST " +
                r.score;
        }

        row.appendChild(badge);

        peerList.appendChild(row);

        const securityRow =
            document.createElement("div");

        securityRow.className =
            "peer-row";

        securityRow.innerHTML =
            "<div><b>" +
            id +
            "</b><br><small>Trust score: " +
            r.score +
            " • Violations: " +
            r.violations +
            "</small></div>";

        const button =
            document.createElement("button");

        button.className =
            "danger";

        button.textContent =
            "Quarantine";

        button.onclick =
            () => quarantinePeer(id);

        securityRow.appendChild(button);

        securityPeers.appendChild(securityRow);
    });

    updateTrustScore();
}

function copyPeerId() {

    const id =
        document.getElementById("myPeerId").textContent;

    if(id && id !== "...") {

        navigator.clipboard.writeText(id);

        setStatus("Peer ID copied to clipboard.");

    }
}

initPeer();

setInterval(
    renderPeers,
    1000
);

</script>

</body>
</html>
"""

components.html(
    html,
    height=1250,
    scrolling=True
)

st.divider()
