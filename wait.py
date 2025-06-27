import streamlit as

<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WAITT – we're all in this together</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
            overflow-x: hidden;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            padding: 20px 0;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            position: sticky;
            top: 0;
            z-index: 100;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            font-size: 2rem;
            font-weight: 700;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .nav-tabs {
            display: flex;
            gap: 10px;
            background: rgba(255, 255, 255, 0.1);
            padding: 8px;
            border-radius: 50px;
            backdrop-filter: blur(10px);
        }
        
        .nav-tab {
            padding: 12px 24px;
            border: none;
            background: transparent;
            color: #666;
            cursor: pointer;
            border-radius: 50px;
            font-weight: 500;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .nav-tab.active {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        
        .nav-tab:hover:not(.active) {
            background: rgba(102, 126, 234, 0.1);
            color: #667eea;
        }
        
        .main-content {
            padding: 40px 0;
        }
        
        .tab-content {
            display: none;
            animation: slideIn 0.5s ease-out;
        }
        
        .tab-content.active {
            display: block;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .section-title {
            font-size: 2rem;
            font-weight: 600;
            margin-bottom: 30px;
            text-align: center;
            color: white;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .groups-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }
        
        .group-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
        }
        
        .group-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #667eea, #764ba2);
        }
        
        .group-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }
        
        .group-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .group-icon {
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
        }
        
        .group-title {
            font-size: 1.3rem;
            font-weight: 600;
            color: #333;
        }
        
        .group-meta {
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
            font-size: 0.9rem;
            color: #666;
        }
        
        .meta-item {
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .group-question {
            background: #f8f9ff;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
            border-left: 4px solid #667eea;
        }
        
        .question-label {
            font-size: 0.85rem;
            font-weight: 600;
            color: #667eea;
            margin-bottom: 8px;
        }
        
        .question-text {
            font-style: italic;
            color: #555;
        }
        
        .answer-input {
            width: 100%;
            padding: 15px;
            border: 2px solid #e1e5e9;
            border-radius: 12px;
            font-size: 1rem;
            margin-bottom: 15px;
            transition: all 0.3s ease;
            resize: vertical;
            min-height: 80px;
        }
        
        .answer-input:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .join-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .join-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        }
        
        .join-btn:active {
            transform: translateY(0);
        }
        
        .join-btn.joined {
            background: #10b981;
            cursor: default;
        }
        
        .spaces-indicator {
            display: inline-flex;
            align-items: center;
            background: #e1f5fe;
            color: #0277bd;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        }
        
        .create-form {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 40px;
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            max-width: 600px;
            margin: 0 auto;
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        .form-label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
        }
        
        .form-input, .form-select {
            width: 100%;
            padding: 15px;
            border: 2px solid #e1e5e9;
            border-radius: 12px;
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        
        .form-input:focus, .form-select:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .slider-container {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .slider {
            flex: 1;
            height: 6px;
            border-radius: 3px;
            background: #e1e5e9;
            outline: none;
            -webkit-appearance: none;
        }
        
        .slider::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea, #764ba2);
            cursor: pointer;
        }
        
        .slider-value {
            background: #667eea;
            color: white;
            padding: 8px 12px;
            border-radius: 20px;
            font-weight: 600;
            min-width: 40px;
            text-align: center;
        }
        
        .create-btn {
            width: 100%;
            padding: 18px;
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .create-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(16, 185, 129, 0.4);
        }
        
        .my-groups-list {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        
        .my-group-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 16px;
            padding: 25px;
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-left: 5px solid #10b981;
        }
        
        .group-members {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 15px 0;
        }
        
        .member-tag {
            background: #f0f9ff;
            color: #0369a1;
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 500;
        }
        
        .answers-section {
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #e5e7eb;
        }
        
        .answer-item {
            background: #fafafa;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 10px;
            border-left: 3px solid #667eea;
        }
        
        .answer-author {
            font-weight: 600;
            color: #667eea;
            margin-bottom: 5px;
        }
        
        .pinnwand {
            max-width: 800px;
            margin: 0 auto;
        }
        
        .question-of-week {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 40px;
            text-align: center;
            margin-bottom: 40px;
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .week-question {
            font-size: 1.4rem;
            font-weight: 600;
            color: #333;
            margin-bottom: 25px;
        }
        
        .answer-area {
            width: 100%;
            min-height: 100px;
            padding: 20px;
            border: 2px solid #e1e5e9;
            border-radius: 16px;
            font-size: 1rem;
            margin-bottom: 20px;
            resize: vertical;
            transition: all 0.3s ease;
        }
        
        .answer-area:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .submit-btn {
            padding: 15px 40px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 50px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
        }
        
        .postits-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        
        .postit {
            background: #fef3c7;
            padding: 20px;
            border-radius: 12px;
            transform: rotate(-1deg);
            transition: all 0.3s ease;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            position: relative;
        }
        
        .postit:nth-child(2n) {
            transform: rotate(1deg);
            background: #dcfce7;
        }
        
        .postit:nth-child(3n) {
            transform: rotate(-0.5deg);
            background: #fce7f3;
        }
        
        .postit:hover {
            transform: rotate(0deg) scale(1.05);
            z-index: 10;
        }
        
        .postit::before {
            content: '📌';
            position: absolute;
            top: -10px;
            right: 15px;
            font-size: 1.5rem;
        }
        
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 25px;
            border-radius: 12px;
            color: white;
            font-weight: 500;
            z-index: 1000;
            transform: translateX(400px);
            transition: all 0.3s ease;
        }
        
        .notification.success {
            background: #10b981;
        }
        
        .notification.warning {
            background: #f59e0b;
        }
        
        .notification.show {
            transform: translateX(0);
        }
        
        @media (max-width: 768px) {
            .header-content {
                flex-direction: column;
                gap: 20px;
            }
            
            .nav-tabs {
                width: 100%;
                justify-content: center;
                flex-wrap: wrap;
            }
            
            .nav-tab {
                padding: 10px 16px;
                font-size: 0.9rem;
            }
            
            .groups-grid {
                grid-template-columns: 1fr;
            }
            
            .group-card {
                padding: 20px;
            }
            
            .create-form {
                padding: 25px;
                margin: 0 10px;
            }
            
            .section-title {
                font-size: 1.5rem;
            }
        }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <div class="header-content">
                <div class="logo">WAITT</div>
                <nav class="nav-tabs">
                    <button class="nav-tab active" onclick="switchTab('find')">Gruppen finden</button>
                    <button class="nav-tab" onclick="switchTab('create')">Erstellen</button>
                    <button class="nav-tab" onclick="switchTab('my')">Meine Gruppen</button>
                    <button class="nav-tab" onclick="switchTab('pinnwand')">Pinnwand</button>
                </nav>
            </div>
        </div>
    </header>

    <main class="main-content">
        <div class="container">
            <!-- Tab: Gruppen finden -->
            <div id="find-tab" class="tab-content active">
                <h2 class="section-title">Offene Lerngruppen</h2>
                <div class="groups-grid" id="groups-container">
                    <!-- Gruppen werden hier dynamisch eingefügt -->
                </div>
            </div>

            <!-- Tab: Gruppe erstellen -->
            <div id="create-tab" class="tab-content">
                <h2 class="section-title">Neue Lerngruppe erstellen</h2>
                <div class="create-form">
                    <div class="form-group">
                        <label class="form-label">Thema</label>
                        <input type="text" class="form-input" id="topic-input" placeholder="z.B. Statistik Klausur">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Uhrzeit</label>
                        <input type="time" class="form-input" id="time-input">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Ort</label>
                        <select class="form-select" id="room-input">
                            <option value="Raum A1">Raum A1</option>
                            <option value="Raum A2">Raum A2</option>
                            <option value="Bibliothek Gruppenraum">Bibliothek Gruppenraum</option>
                            <option value="Café Campus">Café Campus</option>
                            <option value="Lernwiese">Lernwiese</option>
                            <option value="Online">Online</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Maximale Teilnehmerzahl</label>
                        <div class="slider-container">
                            <input type="range" class="slider" id="max-slider" min="2" max="10" value="4">
                            <div class="slider-value" id="max-value">4</div>
                        </div>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Einstiegsfrage</label>
                        <textarea class="form-input" id="question-input" rows="3" placeholder="Was möchtest du von deiner Gruppe wissen?"></textarea>
                    </div>
                    <button class="create-btn" onclick="createGroup()">Gruppe erstellen</button>
                </div>
            </div>

            <!-- Tab: Meine Gruppen -->
            <div id="my-tab" class="tab-content">
                <h2 class="section-title">Deine Gruppen</h2>
                <div class="my-groups-list" id="my-groups-container">
                    <!-- Meine Gruppen werden hier angezeigt -->
                </div>
            </div>

            <!-- Tab: Pinnwand -->
            <div id="pinnwand-tab" class="tab-content">
                <div class="pinnwand">
                    <h2 class="section-title">Community Pinnwand</h2>
                    <div class="question-of-week">
                        <div class="week-question" id="current-question">Was gibt dir gerade Energie beim Lernen?</div>
                        <textarea class="answer-area" id="pinnwand-answer" placeholder="Teile deine Gedanken mit der Community..."></textarea>
                        <button class="submit-btn" onclick="submitPinnwandAnswer()">Antwort teilen</button>
                    </div>
                    <div class="postits-grid" id="postits-container">
                        <!-- Post-its werden hier angezeigt -->
                    </div>
                </div>
            </div>
        </div>
    </main>

    <div id="notification" class="notification"></div>

    <script>
        // Datenstrukturen
        let groups = [
            {
                id: 1,
                topic: "Statistik Klausur",
                time: "10:00",
                room: "Raum A1",
                max: 4,
                members: ["Anna", "Ben"],
                question: "Was ist deine größte Prokrastinationsgefahr?",
                answers: {"Anna": "Netflix und Social Media", "Ben": "Perfektionismus bei Aufgaben"},
                icon: "📊"
            },
            {
                id: 2,
                topic: "Klinische Psychologie",
                time: "14:30",
                room: "Bibliothek Gruppenraum 2",
                max: 3,
                members: ["Chris"],
                question: "Was motiviert dich heute zu lernen?",
                answers: {"Chris": "Die Aussicht auf bessere Berufschancen"},
                icon: "🧠"
            },
            {
                id: 3,
                topic: "Biopsychologie",
                time: "09:00",
                room: "Café Campus",
                max: 5,
                members: [],
                question: "Wenn dein Gehirn eine Farbe hätte – welche?",
                answers: {},
                icon: "🔬"
            }
        ];

        let joinedGroups = [];
        let pinnwandEntries = [
            "Gute Musik und der Gedanke an die Ferien",
            "Lerngruppen wie diese hier!",
            "Kaffee und die Aussicht auf Erfolg"
        ];

        // Tab-Switching
        function switchTab(tabName) {
            // Alle Tabs verstecken
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Alle Tab-Buttons deaktivieren
            document.querySelectorAll('.nav-tab').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Gewählten Tab anzeigen
            document.getElementById(tabName + '-tab').classList.add('active');
            event.target.classList.add('active');
            
            // Content laden
            if (tabName === 'find') renderGroups();
            if (tabName === 'my') renderMyGroups();
            if (tabName === 'pinnwand') renderPinnwand();
        }

        // Gruppen rendern
        function renderGroups() {
            const container = document.getElementById('groups-container');
            container.innerHTML = '';
            
            groups.forEach(group => {
                const freeSpaces = group.max - group.members.length;
                const isJoined = joinedGroups.includes(group.id);
                
                const groupCard = document.createElement('div');
                groupCard.className = 'group-card';
                groupCard.innerHTML = `
                    <div class="group-header">
                        <div class="group-icon">${group.icon}</div>
                        <div>
                            <div class="group-title">${group.topic}</div>
                            <div class="spaces-indicator">${freeSpaces} freie Plätze</div>
                        </div>
                    </div>
                    <div class="group-meta">
                        <div class="meta-item">🕐 ${group.time}</div>
                        <div class="meta-item">📍 ${group.room}</div>
                        <div class="meta-item">👥 ${group.members.length}/${group.max}</div>
                    </div>
                    <div class="group-question">
                        <div class="question-label">Einstiegsfrage</div>
                        <div class="question-text">${group.question}</div>
                    </div>
                    ${!isJoined ? `
                        <textarea class="answer-input" id="answer-${group.id}" placeholder="Deine Antwort auf die Einstiegsfrage..."></textarea>
                        <button class="join-btn" onclick="joinGroup(${group.id})">🚀 Gruppe beitreten</button>
                    ` : `
                        <button class="join-btn joined">✓ Bereits beigetreten</button>
                    `}
                `;
                container.appendChild(groupCard);
            });
        }

        // Gruppe beitreten
        function joinGroup(groupId) {
            const answerField = document.getElementById(`answer-${groupId}`);
            const answer = answerField.value.trim();
            
            if (!answer) {
                showNotification('Bitte beantworte die Einstiegsfrage.', 'warning');
                return;
            }
            
            const group = groups.find(g => g.id === groupId);
            if (group && !joinedGroups.includes(groupId)) {
                group.members.push('Du');
                group.answers['Du'] = answer;
                joinedGroups.push(groupId);
                
                showNotification('Erfolgreich der Gruppe beigetreten!', 'success');
                renderGroups();
            }
        }

        // Neue Gruppe erstellen
        function createGroup() {
            const topic = document.getElementById('topic-input').value.trim();
            const time = document.getElementById('time-input').value;
            const room = document.getElementById('room-input').value;
            const max = parseInt(document.getElementById('max-slider').value);
            const question = document.getElementById('question-input').value.trim();
            
            if (!topic || !time || !question) {
                showNotification('Bitte fülle alle Pflichtfelder aus.', 'warning');
                return;
            }
            
            const icons = ['📚', '🔬', '💡', '🎯', '🧮', '🎨', '🌟', '⚡'];
            const newGroup = {
                id: Date.now(),
                topic,
                time,
                room,
                max,
                members: ['Du'],
                question,
                answers: {'Du': '(Gruppengründer)'},
                icon: icons[Math.floor(Math.random() * icons.length)]
            };
            
            groups.push(newGroup);
            joinedGroups.push(newGroup.id);
            
            // Formular zurücksetzen
            document.getElementById('topic-input').value = '';
            document.getElementById('time-input').value = '';
            document.getElementById('question-input').value = '';
            
            showNotification('Gruppe erfolgreich erstellt!', 'success');
            switchTab('my');
        }

        // Meine Gruppen rendern
        function renderMyGroups() {
            const container = document.getElementById('my-groups-container');
            container.innerHTML = '';
            
            const myGroups = groups.filter(group => joinedGroups.includes(group.id));
            
            if (myGroups.length === 0) {
                container.innerHTML = `
                    <div style="text-align: center; padding: 40px; color: white;">
                        <h3>Du bist noch keiner Gruppe beigetreten</h3>
                        <p>Schau doch mal bei "Gruppen finden" vorbei!</p>
                    </div>
                `;
                return;
            }
            
            myGroups.forEach(group => {
                const groupCard = document.createElement('div');
                groupCard.className = 'my-group-card';
                groupCard.innerHTML = `
                    <div class="group-header">
                        <div class="group-icon">${group.icon}</div>
                        <div>
                            <div class="group-title">${group.topic}</div>
                            <div class="group-meta">
                                <div class="meta-item">🕐 ${group.time}</div>
                                <div class="meta-item">📍 ${group.room}</div>
                            </div>
                        </div>
                    </div>
                    <div class="group-members">
                        ${group.members.map(member => `<span class="member-tag">${member}</span>`).join('')}
                    </div>
                    <div class="answers-section">
                        <h4>Antworten auf: "${group.question}"
