# Main Navigation Tabs
    tabs = st.tabs([
        "🌿 Pausengestaltung",
        "🔍 Gruppen finden", 
        "➕ Gruppe erstellen", 
        "👥 Meine Gruppen", 
        "📌 Community-Pinnwand"
    ])
    
    # Tab 1: Pausengestaltung (NEW - Primary Focus)
    with tabs[0]:
        st.markdown("# 🌿 Gesunde Pausen für Körper & Geist")
        
        info_html = """
        <div class="card" style="background: linear-gradient(135deg, #DBEAFE, #E0E7FF);">
            <p style="margin: 0; line-height: 1.6;">
                <strong>Du bist nicht allein!</strong> Viele Studierende kämpfen mit dem Gefühl, 
                nie genug zu tun. Diese Pausen helfen dir, aus dem Hamsterrad auszusteigen 
                und wieder Freude am Studium zu finden. 💙
            </p>
        </div>
        """
        st.markdown(info_html, unsafe_allow_html=True)
        
        # Pause Statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">{st.session_state.pause_statistics["solo_pausen"]}</div>
                <div class="metric-label">Solo-Pausen</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">{st.session_state.pause_statistics["wakenitz_besuche"]}</div>
                <div class="metric-label">Natur-Momente</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">{st.session_state.pause_statistics["bewegung_minuten"]}</div>
                <div class="metric-label">Minuten bewegt</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-container">
                <div class="metric-value">{st.session_state.pause_statistics["meditation_minuten"]}</div>
                <div class="metric-label">Minuten Ruhe</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 2-Minute Countdown Section
        st.markdown("### 🧘 Sofort-Entspannung: Die 2-Minuten-Challenge")
        render_countdown_timer()
        
        st.markdown("---")
        
        # Activity Selection
        st.markdown("### 🎯 Deine persönliche Pause")
        
        pause_type = st.radio(
            "Wie möchtest du deine Pause verbringen?",
            ["🧘 Solo-Pause (Zeit für mich)", "👥 Gruppen-Pause (Gemeinsam entspannen)"],
            horizontal=True,
            help="Beide Arten sind wichtig für deine mentale Gesundheit!"
        )
        
        activities = get_luebeck_activities()
        
        if "Solo-Pause" in pause_type:
            st.markdown("#### 🌊 Solo-Aktivitäten in Lübeck")
            
            # Quick selection buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🌿 Natur", use_container_width=True):
                    nature_activities = [a for a in activities["solo"] if "Natur" in a["type"]]
                    if nature_activities:
                        st.session_state.current_solo_activity = random.choice(nature_activities)
            
            with col2:
                if st.button("🏃 Bewegung", use_container_width=True):
                    movement_activities = [a for a in activities["solo"] if "Bewegung" in a["type"]]
                    if movement_activities:
                        st.session_state.current_solo_activity = random.choice(movement_activities)
            
            with col3:
                if st.button("⚡ Schnell", use_container_width=True):
                    quick_activities = [a for a in activities["solo"] if int(a["duration"].split()[0]) <= 5]
                    if quick_activities:
                        st.session_state.current_solo_activity = random.choice(quick_activities)
            
            # Random activity button
            if st.button("🎲 Zufällige Solo-Aktivität vorschlagen", use_container_width=True):
                st.session_state.current_solo_activity = random.choice(activities["solo"])
            
            # Display selected activity
            if st.session_state.current_solo_activity:
                render_pause_activity_card(st.session_state.current_solo_activity, "solo")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Pause gemacht!", key="solo_done", use_container_width=True):
                        activity = st.session_state.current_solo_activity
                        
                        # Update statistics
                        st.session_state.pause_statistics["solo_pausen"] += 1
                        duration = int(activity['duration'].split()[0])
                        st.session_state.pause_statistics["total_time"] += duration
                        
                        # Track specific activities
                        if "wakenitz" in activity['name'].lower():
                            st.session_state.pause_statistics["wakenitz_besuche"] += 1
                        if "trave" in activity['name'].lower():
                            st.session_state.pause_statistics["trave_spaziergaenge"] += 1
                        if "Bewegung" in activity['type']:
                            st.session_state.pause_statistics["bewegung_minuten"] += duration
                        if "Achtsamkeit" in activity['type'] or "meditation" in activity['name'].lower():
                            st.session_state.pause_statistics["meditation_minuten"] += duration
                        
                        # Add stamps
                        for _ in range(activity['stamps']):
                            add_reward_stamp("solo_activity")
                        
                        # Motivational message
                        messages = [
                            f"Großartig! Diese {duration} Minuten waren eine Investition in deine Gesundheit! 🌟",
                            f"Super! Du hast dir {duration} Minuten gegönnt - du hast es verdient! 💪",
                            f"Toll gemacht! +{activity['stamps']} Stempel für deine Selbstfürsorge! 🎯",
                            f"Perfekt! Diese Pause macht dich stärker für die nächste Lerneinheit! 🚀"
                        ]
                        show_success_message(random.choice(messages))
                        
                        # Reset activity
                        st.session_state.current_solo_activity = None
                        st.rerun()
                
                with col2:
                    if st.button("🔄 Andere Aktivität", key="solo_new", use_container_width=True):
                        st.session_state.current_solo_activity = random.choice(activities["solo"])
                        st.rerun()
        
        else:  # Group activities
            st.markdown("#### 👥 Gruppen-Aktivitäten in Lübeck")
            
            # Check if user is in any groups
            my_groups = [g for g in st.session_state.groups if g["id"] in st.session_state.joined_groups]
            
            if not my_groups:
                warning_html = """
                <div class="card" style="background: linear-gradient(135deg, #FEF3C7, #FDE68A);">
                    <p style="margin: 0; color: #92400E;">
                        <strong>💡 Tipp:</strong> Tritt erst einer Lerngruppe bei oder erstelle eine eigene, 
                        um Gruppenpausen zu planen! Gemeinsame Pausen helfen gegen Einsamkeit und machen mehr Spaß.
                    </p>
                </div>
                """
                st.markdown(warning_html, unsafe_allow_html=True)
                
                if st.button("→ Zu den Lerngruppen", use_container_width=True):
                    st.write("Wechsle zum Tab 'Gruppen finden'!")
            
            else:
                # Group selection
                selected_group = st.selectbox(
                    "Mit welcher Lerngruppe möchtest du eine Pause machen?",
                    options=[g["topic"] for g in my_groups],
                    help="Wähle die Gruppe aus, mit der du gemeinsam pausieren möchtest"
                )
                
                # Activity categories for groups
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("🌳 Outdoor", use_container_width=True):
                        outdoor_activities = [a for a in activities["gruppe"] if "Natur" in a["type"] or "Sport" in a["type"]]
                        if outdoor_activities:
                            st.session_state.current_group_activity = random.choice(outdoor_activities)
                
                with col2:
                    if st.button("💬 Reden", use_container_width=True):
                        talk_activities = [a for a in activities["gruppe"] if "Talk" in a["name"] or "Soziale" in a["type"]]
                        if talk_activities:
                            st.session_state.current_group_activity = random.choice(talk_activities)
                
                with col3:
                    if st.button("🎮 Spielen", use_container_width=True):
                        game_activities = [a for a in activities["gruppe"] if "Rallye" in a["name"] or "Olympics" in a["name"]]
                        if game_activities:
                            st.session_state.current_group_activity = random.choice(game_activities)
                
                # Random group activity
                if st.button("🎲 Zufällige Gruppen-Aktivität vorschlagen", use_container_width=True):
                    st.session_state.current_group_activity = random.choice(activities["gruppe"])
                
                # Display selected activity
                if st.session_state.current_group_activity:
                    render_pause_activity_card(st.session_state.current_group_activity, "gruppe")
                    
                    # Sharing functionality
                    st.markdown("##### 📤 Aktivität mit der Gruppe teilen:")
                    share_message = f"""
Hey {selected_group}-Gruppe! 👋

Ich schlage vor, wir machen eine gemeinsame Pause:

**{st.session_state.current_group_activity['name']}**
📍 Ort: {st.session_state.current_group_activity['location']}
⏱️ Dauer: {st.session_state.current_group_activity['duration']}

Wer ist dabei? 🙋‍♀️🙋‍♂️
                    """
                    
                    st.text_area("Nachricht an die Gruppe:", value=share_message, height=150)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ Pause durchgeführt!", key="group_done", use_container_width=True):
                            activity = st.session_state.current_group_activity
                            
                            # Update statistics
                            st.session_state.pause_statistics["gruppen_pausen"] += 1
                            duration = int(activity['duration'].split()[0])
                            st.session_state.pause_statistics["total_time"] += duration
                            
                            # Add extra stats for group activities
                            if "wakenitz" in activity['name'].lower():
                                st.session_state.pause_statistics["wakenitz_besuche"] += 1
                            if "trave" in activity['name'].lower():
                                st.session_state.pause_statistics["trave_spaziergaenge"] += 1
                            if "Sport" in activity['type'] or "Bewegung" in activity['type']:
                                st.session_state.pause_statistics["bewegung_minuten"] += duration
                            
                            # Add stamps (group activities give more!)
                            for _ in range(activity['stamps']):
                                add_reward_stamp("group_activity")
                            
                            # Special message for group activities
                            messages = [
                                f"Fantastisch! Ihr habt gemeinsam {duration} Minuten Auszeit genommen! 🤝",
                                f"Teamwork! +{activity['stamps']} Stempel für eure gemeinsame Pause! 🌟",
                                f"Ihr seid ein tolles Team! Diese Pause stärkt eure Verbindung! 💪",
                                f"Gemeinsam stark! Diese {duration} Minuten waren Gold wert! 🏆"
                            ]
                            show_success_message(random.choice(messages))
                            
                            # Reset activity
                            st.session_state.current_group_activity = None
                            st.rerun()
                    
                    with col2:
                        if st.button("🔄 Andere Aktivität", key="group_new", use_container_width=True):
                            st.session_state.current_group_activity = random.choice(activities["gruppe"])
                            st.rerun()
        
        # Wellness Tips Section
        st.markdown("---")
        st.markdown("### 💡 Warum Pausen so wichtig sind")
        
        tips_html = """
        <div class="card">
            <h4 style="color: #059669; margin-bottom: 1rem;">🧠 Wissenschaftlich bewiesen:</h4>
            <ul style="line-height: 1.8; color: #4B5563;">
                <li><strong>90-Minuten-Regel:</strong> Unser Gehirn kann maximal 90 Minuten konzentriert arbeiten</li>
                <li><strong>20-20-20:</strong> Alle 20 Min für 20 Sek auf etwas 20 Fuß (6m) Entferntes schauen</li>
                <li><strong>Bewegung:</strong> 5 Min Bewegung steigert die Konzentration um 23%</li>
                <li><strong>Natur:</strong> 10 Min in der Natur senken Stresshormone um 15%</li>
                <li><strong>Soziale Pausen:</strong> Reduzieren das Burnout-Risiko um 40%</li>
            </ul>
        </div>
        """
        st.markdown(tips_html, unsafe_allow_html=True)
    
    # Tab 4: My Groups
    with tabs[3]:
        st.markdown("## 👥 Deine Lerngruppen & Verbindungen")
        
        my_groups = [g for g in st.session_state.groups if g["id"] in st.session_state.joined_groups]
        
        if not my_groups:
            empty_html = """
            <div class="card" style="text-align: center; padding: 3rem;">
                <h3 style="color: #6B7280; margin-bottom: 1rem;">Du bist noch in keiner Gruppe 😔</h3>
                <p style="color: #9CA3AF; margin-bottom: 2rem;">
                    Lerngruppen helfen nicht nur beim Studium - sie sind auch ein Schutz gegen Einsamkeit!<br>
                    Finde Menschen, die ähnliche Herausforderungen haben wie du.
                </p>
                <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
                    <span style="background: #E0E7FF; color: #4338CA; padding: 0.5rem 1rem; border-radius: 20px;">
                        🤝 Gemeinsam stärker
                    </span>
                    <span style="background: #FEE2E2; color: #DC2626; padding: 0.5rem 1rem; border-radius: 20px;">
                        ❤️ Weniger allein
                    </span>
                    <span style="background: #D1FAE5; color: #059669; padding: 0.5rem 1rem; border-radius: 20px;">
                        🎯 Mehr Motivation
                    </span>
                </div>
            </div>
            """
            st.markdown(empty_html, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔍 Gruppe finden", use_container_width=True):
                    st.info("Wechsle zum Tab 'Gruppen finden'!")
            with col2:
                if st.button("➕ Gruppe gründen", use_container_width=True):
                    st.info("Wechsle zum Tab 'Gruppe erstellen'!")
        
        else:
            # Group overview
            overview_html = f"""
            <div class="card" style="background: linear-gradient(135deg, #EDE9FE, #DDD6FE); margin-bottom: 1rem;">
                <p style="margin: 0; color: #5B21B6;">
                    <strong>Du bist Teil von {len(my_groups)} Gruppe{'n' if len(my_groups) > 1 else ''}!</strong> 
                    Das sind {len(my_groups) * 3} bis {len(my_groups) * 5} Menschen, die dich unterstützen. 💜
                </p>
            </div>
            """
            st.markdown(overview_html, unsafe_allow_html=True)
            
            for group in my_groups:
                group_html = f"""
                <div class="card" style="border-left: 4px solid {get_group_card_class(group.get('category', 'other'))};">
                    <div class="group-header">
                        <div class="group-icon">{group["icon"]}</div>
                        <div class="group-content">
                            <h3 class="group-title">{group["topic"]}</h3>
                            <div class="group-meta">
                                <div class="meta-item">🕐 {group["time"]}</div>
                                <div class="meta-item">📍 {group["room"]}</div>
                                <div class="meta-item">👥 {len(group["members"])}/{group["max"]}</div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="question-box" style="margin-top: 1rem;">
                        <div class="question-label">Eure Einstiegsfrage</div>
                        <div class="question-text">"{group["question"]}"</div>
                    </div>
                </div>
                """
                st.markdown(group_html, unsafe_allow_html=True)
                
                # Members section
                st.markdown("#### Gruppenmitglieder:")
                members_html = '<div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin: 1rem 0;">'
                for member in group["members"]:
                    members_html += f'<span class="member-tag">{member}</span>'
                members_html += '</div>'
                st.markdown(members_html, unsafe_allow_html=True)
                
                # Answers section
                if group["answers"]:
                    with st.expander(f"💬 Alle Antworten ansehen ({len(group['answers'])})"):
                        for name, answer in group["answers"].items():
                            answer_html = f"""
                            <div class="answer-item">
                                <div class="answer-author">{name}</div>
                                <div style="color: #4B5563;">"{answer}"</div>
                            </div>
                            """
                            st.markdown(answer_html, unsafe_allow_html=True)
                
                # Group actions
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button(f"🌿 Gruppenpause", key=f"pause_{group['id']}", use_container_width=True):
                        activities = get_luebeck_activities()["gruppe"]
                        activity = random.choice(activities)
                        
                        pause_html = f"""
                        <div class="activity-card" style="margin-top: 1rem;">
                            <h4 style="color: #059669;">Pausenvorschlag für eure Gruppe:</h4>
                            <h3 style="color: #831843; margin: 0.5rem 0;">{activity['name']}</h3>
                            <p><strong>📍 {activity['location']}</strong> | ⏱️ {activity['duration']}</p>
                            <p style="margin: 0.5rem 0;">{activity['description']}</p>
                        </div>
                        """
                        st.markdown(pause_html, unsafe_allow_html=True)
                        
                        if st.button(f"✅ Gemacht!", key=f"done_{group['id']}_pause"):
                            st.session_state.pause_statistics["gruppen_pausen"] += 1
                            st.session_state.pause_statistics["total_time"] += int(activity['duration'].split()[0])
                            for _ in range(activity['stamps']):
                                add_reward_stamp("group_activity")
                            show_success_message(f"Super! Die Pause hat euch gutgetan! +{activity['stamps']} Stempel")
                            st.rerun()
                
                with col2:
                    if st.button(f"💬 Nachricht", key=f"msg_{group['id']}", use_container_width=True):
                        st.text_area(
                            "Nachricht an die Gruppe:",
                            placeholder="Hey Leute, wie wär's mit...",
                            key=f"msg_text_{group['id']}"
                        )
                
                with col3:
                    if st.button(f"🚪 Verlassen", key=f"leave_{group['id']}", use_container_width=True):
                        if st.checkbox(f"Wirklich '{group['topic']}' verlassen?", key=f"confirm_{group['id']}"):
                            if "Du" in group["members"]:
                                group["members"].remove("Du")
                            if "Du" in group["answers"]:
                                del group["answers"]["Du"]
                            st.session_state.joined_groups.remove(group["id"])
                            show_info_message("Du hast die Gruppe verlassen. Du kannst jederzeit wieder beitreten!")
                            st.rerun()
                
                st.markdown("---")
    
    # Tab 5: Community Board
    with tabs[4]:
        st.markdown("## 📌 Community-Pinnwand")
        
        # Current question of the week
        question_html = f"""
        <div class="card" style="background: linear-gradient(135deg, #FDF2F8, #FCE7F3); border: 2px solid #F9A8D4;">
            <h3 style="color: #831843; margin-bottom: 0.5rem; text-align: center;">🌟 Frage der Woche</h3>
            <h2 style="color: #BE185D; text-align: center; margin: 0;">"{st.session_state.current_question}"</h2>
        </div>
        """
        st.markdown(question_html, unsafe_allow_html=True)
        
        # Add entry form
        with st.form("pinnwand_form", clear_on_submit=True):
            new_entry = st.text_area(
                "💭 Deine Antwort:",
                placeholder="Teile deine Gedanken mit der Community...",
                height=100,
                help="Deine Erfahrungen können anderen helfen!"
            )
            
            col1, col2 = st.columns([3, 1])
            with col1:
                submitted = st.form_submit_button("📌 An Pinnwand heften", use_container_width=True)
            with col2:
                anonymous = st.checkbox("Anonym posten")
            
            if submitted:
                if new_entry.strip():
                    st.session_state.pinnwand_entries.append(new_entry.strip())
                    add_reward_stamp("pinnwand_post")
                    show_success_message("Dein Beitrag wurde angepinnt! Danke fürs Teilen! 💝")
                    st.rerun()
                else:
                    show_warning_message("Schreibe etwas, das anderen Mut machen könnte!")
        
        # Display entries
        st.markdown("### 💬 Was die Community sagt:")
        
        if st.session_state.pinnwand_entries:
            # Create 2-column layout for entries
            entries = st.session_state.pinnwand_entries
            cols = st.columns(2)
            
            colors = [
                ("#fef3c7", "#f59e0b", "-1deg"),
                ("#dcfce7", "#10b981", "1deg"), 
                ("#fce7f3", "#ec4899", "-0.5deg"),
                ("#dbeafe", "#3b82f6", "0.8deg"),
                ("#fae8ff", "#a855f7", "-0.8deg"),
                ("#ffedd5", "#fb923c", "0.5deg")
            ]
            
            for idx, entry in enumerate(entries):
                col_idx = idx % 2
                bg_color, border_color, rotation = colors[idx % len(colors)]
                
                with cols[col_idx]:
                    entry_html = f"""
                    <div class="pinnwand-entry" style="
                        background: {bg_color};
                        border: 1px solid {border_color};
                        transform: rotate({rotation});
                    ">
                        <div class="pin-icon">📌</div>
                        <p style="margin: 0; font-size: 0.95rem; line-height: 1.6; color: #374151;">
                            "{entry}"
                        </p>
                        <div style="text-align: right; margin-top: 0.5rem;">
                            <small style="color: #6B7280; font-style: italic;">
                                - {"Anonym" if idx % 3 == 0 else f"Student:in #{idx+1}"}
                            </small>
                        </div>
                    </div>
                    """
                    st.markdown(entry_html, unsafe_allow_html=True)
        else:
            st.info("Sei der/die Erste und teile deine Gedanken! 📝")
        
        # Motivational quotes section
        st.markdown("---")
        st.markdown("### 💪 Motivation für schwere Zeiten")
        
        quotes = [
            ("Du schaffst das nicht TROTZ der Herausforderungen, sondern WEGEN ihnen.", "Unbekannt"),
            ("Fortschritt ist wichtiger als Perfektion.", "Studierendenberatung Lübeck"),
            ("Eine Pause ist kein Zeichen von Schwäche, sondern von Weisheit.", "WAITT Team"),
            ("Gemeinsam durch dick und dünn - das ist der Lübecker Weg!", "Hansestadt-Motto"),
            ("Dein Wert hängt nicht von deinen Noten ab.", "Psychologische Beratung")
        ]
        
        quote, author = random.choice(quotes)
        quote_html = f"""
        <div class="card" style="text-align: center; background: linear-gradient(135deg, #F3E8FF, #E9D5FF);">
            <p style="font-size: 1.25rem; font-style: italic; color: #5B21B6; margin: 0;">
                "{quote}"
            </p>
            <p style="margin-top: 0.5rem; color: #7C3AED;">
                - {author}
            </p>
        </div>
        """
        st.markdown(quote_html, unsafe_allow_html=True)
        
        # Admin section (hidden in expander)
        with st.expander("🔧 Pinnwand-Verwaltung (für Admins)"):
            new_question = st.text_input(
                "Neue Frage der Woche:",
                value=st.session_state.current_question
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Frage ändern", use_container_width=True):
                    if new_question.strip() and new_question != st.session_state.current_question:
                        st.session_state.current_question = new_question.strip()
                        show_success_message("Neue Frage der Woche ist aktiv!")
                        st.rerun()
            
            with col2:
                if st.button("🗑️ Alle Einträge löschen", use_container_width=True):
                    if st.checkbox("Wirklich alle Einträge löschen?"):
                        st.session_state.pinnwand_entries = []
                        show_info_message("Pinnwand wurde geleert.")
                        st.rerun()
    
    # Footer with help resources
    st.markdown("---")
    
    # Help section
    help_html = """
    <div class="card" style="background: linear-gradient(135deg, #FEE2E2, #FECACA);">
        <h3 style="color: #991B1B; margin-bottom: 1rem;">🆘 Hilfe & Unterstützung an der Uni Lübeck</h3>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem;">
            <div>
                <h4 style="color: #DC2626;">📞 Psychologische Beratung</h4>
                <p style="font-size: 0.875rem; line-height: 1.6;">
                    <strong>Studentenwerk SH</strong><br>
                    📍 Mönkhofer Weg 241 (Mensagebäude), Raum 44<br>
                    📞 0451 / 29220-908<br>
                    ✉️ psychologen.hl@studentenwerk.sh<br>
                    <em>Kostenlos & vertraulich für alle Studierenden!</em>
                </p>
            </div>
            
            <div>
                <h4 style="color: #DC2626;">🏥 Krisenhilfe (24/7)</h4>
                <p style="font-size: 0.875rem; line-height: 1.6;">
                    <strong>Krisendienst Schleswig-Holstein</strong><br>
                    📞 0800 / 655 3000 (kostenlos)<br><br>
                    <strong>Telefonseelsorge</strong><br>
                    📞 0800 / 111 0 111 oder 0800 / 111 0 222<br>
                    💬 Auch Chat & Mail möglich
                </p>
            </div>
            
            <div>
                <h4 style="color: #DC2626;">🧠 Psychiatrische Hilfe</h4>
                <p style="font-size: 0.875rem; line-height: 1.6;">
                    <strong>Zentrum für Integrative Psychiatrie (ZIP)</strong><br>
                    Dr. Bartosz Zurowski<br>
                    📞 0451 / 500-98831<br>
                    ✉️ bartosz.zurowski@uksh.de<br>
                    <em>Spezielle Sprechstunde für Studierende</em>
                </p>
            </div>
            
            <div>
                <h4 style="color: #DC2626;">💻 Online-Unterstützung</h4>
                <p style="font-size: 0.875rem; line-height: 1.6;">
                    <strong>StudiCare</strong><br>
                    Online-Trainings bei Stress, Prüfungsangst & mehr<br>
                    🌐 www.studicare.com<br><br>
                    <strong>7Mind</strong> - Meditation für Studierende<br>
                    <em>Kostenlos mit Uni-Mail!</em>
                </p>
            </div>
        </div>
        
        <div style="margin-top: 1.5rem; padding: 1rem; background: rgba(220, 38, 38, 0.1); border-radius: 8px;">
            <p style="margin: 0; text-align: center; color: #7F1D1D;">
                <strong>Du bist nicht allein!</strong> Es ist mutig und stark, sich Hilfe zu holen. 
                Deine mentale Gesundheit ist genauso wichtig wie deine körperliche. ❤️
            </p>
        </div>
    </div>
    """
    st.markdown(help_html, unsafe_allow_html=True)
    
    # App info
    st.markdown("---")
    info_html = """
    <div style="text-align: center; color: rgba(255, 255, 255, 0.7); font-size: 0.875rem; padding: 1rem;">
        <p>
            <strong>WAITT - We're All In This Together</strong><br>
            Eine Initiative für mentale Gesundheit und gegen Einsamkeit im Studium<br>
            Made with ❤️ für die Uni Lübeck
        </p>
    </div>
    """
    st.markdown(info_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()html=True)
        
        # Location-specific tips
        luebeck_tips_html = """
        <div class="card" style="background: linear-gradient(135deg, #F3F4F6, #E5E7EB);">
            <h4 style="color: #374151; margin-bottom: 1rem;">📍 Lübeck-Geheimtipps für Pausen:</h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
                <div>
                    <strong style="color: #059669;">🌊 Wasser-Oasen:</strong>
                    <ul style="margin-top: 0.5rem; font-size: 0.875rem;">
                        <li>Wakenitz: "Amazonas des Nordens" - perfekt für Naturpausen</li>
                        <li>Trave-Promenade: Ideal für Walking-Meetings</li>
                        <li>Krähenteich: Versteckter Ruheplatz nahe Altstadt</li>
                    </ul>
                </div>
                <div>
                    <strong style="color: #DC2626;">🏃 Bewegung:</strong>
                    <ul style="margin-top: 0.5rem; font-size: 0.875rem;">
                        <li>Falkenwiese: Slackline, Volleyball, Fitness</li>
                        <li>Wallanlagen: 5km Rundweg um die Altstadt</li>
                        <li>Stadtpark: Trimm-dich-Pfad und Laufstrecken</li>
                    </ul>
                </div>
                <div>
                    <strong style="color: #7C3AED;">☕ Rückzugsorte:</strong>
                    <ul style="margin-top: 0.5rem; font-size: 0.875rem;">
                        <li>Café Affenbrot: Gemütlich in der Altstadt</li>
                        <li>Niederegger: Marzipan-Pause mit Tradition</li>
                        <li>St. Annen-Museum: Ruhiger Innenhof</li>
                    </ul>
                </div>
            </div>
        </div>
        """
        st.markdown(luebeck_tips_html, unsafe_allow_html=True)
        
        # Show reward progress
        if st.session_state.reward_stamps >= 5:
            st.markdown("---")
            st.markdown("### 🏆 Dein Fortschritt")
            render_reward_system()
    
    # Tab 2: Find Groups
    with tabs[1]:
        st.markdown("## 🔍 Lerngruppen finden & vernetzen")
        
        # Emotional appeal
        connect_html = """
        <div class="card" style="background: linear-gradient(135deg, #FEE2E2, #FECACA);">
            <p style="margin: 0; color: #991B1B; line-height: 1.6;">
                <strong>Du fühlst dich allein mit dem Lernstress?</strong> 
                Hier findest du Menschen, die das gleiche durchmachen. 
                Gemeinsam ist man weniger einsam und erfolgreicher! ❤️
            </p>
        </div>
        """
        st.markdown(connect_html, unsafe_allow_html=True)
        
        # Filter options
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            search_term = st.text_input(
                "🔍 Nach Thema suchen",
                placeholder="z.B. Statistik, Anatomie, Psychologie...",
                help="Finde Gruppen zu deinem Fach"
            )
        with col2:
            show_full_only = st.checkbox("Nur freie Plätze", value=True)
        with col3:
            time_filter = st.selectbox(
                "Uhrzeit",
                ["Alle", "Morgens", "Mittags", "Abends"],
                help="Filtere nach Tageszeit"
            )
        
        # Filter groups
        filtered_groups = st.session_state.groups
        
        if search_term:
            filtered_groups = [g for g in filtered_groups if search_term.lower() in g["topic"].lower()]
        
        if show_full_only:
            filtered_groups = [g for g in filtered_groups if len(g["members"]) < g["max"]]
        
        if time_filter != "Alle":
            time_ranges = {
                "Morgens": (6, 12),
                "Mittags": (12, 17),
                "Abends": (17, 23)
            }
            if time_filter in time_ranges:
                min_hour, max_hour = time_ranges[time_filter]
                filtered_groups = [g for g in filtered_groups 
                                 if min_hour <= int(g["time"].split(":")[0]) < max_hour]
        
        # Display groups
        if not filtered_groups:
            st.info("Keine passenden Gruppen gefunden. Erstelle deine eigene!")
        else:
            for group in filtered_groups:
                is_joined, free_spaces = render_group_card(group)
                
                if not is_joined and free_spaces > 0:
                    # Answer input
                    answer = st.text_area(
                        "💭 Beantworte die Einstiegsfrage:",
                        key=f"answer_{group['id']}",
                        height=80,
                        placeholder="Teile deine Gedanken... (Das hilft der Gruppe, dich kennenzulernen!)",
                        help="Eine ehrliche Antwort schafft Verbindung von Anfang an"
                    )
                    
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        if st.button(f"🚀 Gruppe beitreten", key=f"join_{group['id']}", use_container_width=True):
                            if answer.strip():
                                group["members"].append("Du")
                                group["answers"]["Du"] = answer.strip()
                                st.session_state.joined_groups.append(group["id"])
                                add_reward_stamp("group_join")
                                show_success_message("Willkommen in der Gruppe! Ihr seid jetzt verbunden. 🤝")
                                st.rerun()
                            else:
                                show_warning_message("Die Einstiegsfrage hilft, das Eis zu brechen. Probier's nochmal!")
                    
                    with col2:
                        with st.expander("👀 Antworten ansehen"):
                            if group["answers"]:
                                for name, ans in group["answers"].items():
                                    answer_html = f"""
                                    <div class="answer-item">
                                        <div class="answer-author">{name}</div>
                                        <div style="color: #4B5563;">"{ans}"</div>
                                    </div>
                                    """
                                    st.markdown(answer_html, unsafe_allow_html=True)
                            else:
                                st.write("Sei der/die Erste!")
                
                elif is_joined:
                    success_html = """
                    <div style="background: #D1FAE5; padding: 0.75rem; border-radius: 8px; margin-top: 0.5rem;">
                        <span style="color: #065F46;">✅ Du bist Mitglied dieser Gruppe</span>
                    </div>
                    """
                    st.markdown(success_html, unsafe_allow_html=True)
                else:
                    warning_html = """
                    <div style="background: #FEF3C7; padding: 0.75rem; border-radius: 8px; margin-top: 0.5rem;">
                        <span style="color: #92400E;">⏳ Gruppe ist voll - aber vielleicht wird ein Platz frei!</span>
                    </div>
                    """
                    st.markdown(warning_html, unsafe_allow_html=True)
                
                st.markdown("---")
    
    # Tab 3: Create Group
    with tabs[2]:
        create_html = """
        <div class="form-container">
            <h2 class="form-title">🏗️ Deine eigene Lerngruppe gründen</h2>
            <p style="text-align: center; color: #6B7280; margin-bottom: 2rem;">
                Keine passende Gruppe gefunden? Starte deine eigene und finde Gleichgesinnte!
            </p>
        </div>
        """
        st.markdown(create_html, unsafe_allow_html=True)
        
        with st.form("create_group_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                topic = st.text_input(
                    "📚 Thema der Gruppe",
                    placeholder="z.B. 'Statistik II - Gemeinsam schaffen wir das!'",
                    help="Ein motivierender Titel zieht die richtigen Leute an"
                )
                
                time_input = st.time_input(
                    "🕐 Bevorzugte Treffzeit",
                    value=time(14, 0),
                    help="Wann passt es dir am besten?"
                )
                
                room = st.selectbox(
                    "📍 Treffpunkt",
                    get_luebeck_locations(),
                    help="Wo wollt ihr euch treffen?"
                )
            
            with col2:
                max_members = st.slider(
                    "👥 Maximale Gruppengröße",
                    min_value=2,
                    max_value=8,
                    value=4,
                    help="Kleine Gruppen (3-4) sind persönlicher, größere (5-8) dynamischer"
                )
                
                icon = st.selectbox(
                    "🎯 Gruppen-Icon",
                    ["📚", "📊", "🧠", "🔬", "💡", "🎯", "🧮", "🎨", "⚕️", "💻", "🌟", "🚀"],
                    help="Wähle ein Symbol, das zu eurem Thema passt"
                )
                
                category = st.selectbox(
                    "📂 Fachbereich",
                    [
                        ("psychology", "Psychologie"),
                        ("medicine", "Medizin"),
                        ("computer_science", "Informatik/Technik"),
                        ("bio", "Biologie/Naturwissenschaften"),
                        ("stats", "Mathematik/Statistik"),
                        ("other", "Sonstiges")
                    ],
                    format_func=lambda x: x[1],
                    help="Hilft anderen, deine Gruppe zu finden"
                )
            
            st.markdown("#### 💭 Die Einstiegsfrage - Der Eisbrecher")
            question = st.text_area(
                "Stelle eine Frage, die neue Mitglieder beantwortet müssen:",
                placeholder="z.B. 'Was ist dein größtes Hindernis beim Lernen?' oder 'Welche Superkraft hättest du gern für die Klausur?'",
                height=80,
                help="Eine gute Frage schafft sofort Verbindung!"
            )
            
            # Examples for inspiration
            with st.expander("💡 Beispiele für gute Einstiegsfragen"):
                st.markdown("""
                **Persönlich & verbindend:**
                - Was motiviert dich weiterzumachen, wenn's schwer wird?
                - Welcher Lern-Typ bist du: Eule oder Lerche?
                - Was machst du nach bestandener Klausur als Erstes?
                
                **Kreativ & auflockernd:**
                - Wenn dein Lernstress eine Farbe wäre, welche?
                - Welches Tier wärst du in der Klausur und warum?
                - Dein Studium in 3 Emojis?
                
                **Praktisch & hilfreich:**
                - Was ist dein bester Lerntipp, den du teilen möchtest?
                - Wobei brauchst du am meisten Unterstützung?
                - Kaffee oder Tee beim Lernen?
                """)
            
            submitted = st.form_submit_button("🚀 Gruppe erstellen", use_container_width=True)
            
            if submitted:
                if topic.strip() and question.strip():
                    new_group = {
                        "id": str(uuid.uuid4()),
                        "topic": topic.strip(),
                        "time": time_input.strftime("%H:%M"),
                        "room": room,
                        "max": max_members,
                        "members": ["Du"],
                        "question": question.strip(),
                        "answers": {"Du": "(Gruppengründer:in - motiviert und ready!)"},
                        "icon": icon,
                        "category": category[0] if isinstance(category, tuple) else category
                    }
                    
                    st.session_state.groups.append(new_group)
                    st.session_state.joined_groups.append(new_group["id"])
                    add_reward_stamp("group_create")
                    
                    show_success_message(f"Deine Gruppe '{topic}' wurde erstellt! Die ersten werden schon bald dazustoßen. 🎉")
                    st.balloons()
                    pytime.sleep(2)
                    st.rerun()
                else:
                    show_warning_message("Bitte fülle alle Felder aus - deine Gruppe braucht einen Namen und eine Einstiegsfrage!")
        
        # Tips section
        tips_html = """
        <div class="card" style="margin-top: 2rem;">
            <h4 style="color: #059669; margin-bottom: 1rem;">🌟 Tipps für erfolgreiche Lerngruppen:</h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem;">
                <div>
                    <strong>📅 Regelmäßigkeit</strong>
                    <p style="font-size: 0.875rem; margin-top: 0.25rem;">
                        Feste Termine schaffen Verbindlichkeit und Routine
                    </p>
                </div>
                <div>
                    <strong>🎯 Klare Ziele</strong>
                    <p style="font-size: 0.875rem; margin-top: 0.25rem;">
                        Definiert, was ihr gemeinsam erreichen wollt
                    </p>
                </div>
                <div>
                    <strong>⏰ Pausen einplanen</strong>
                    <p style="font-size: 0.875rem; margin-top: 0.25rem;">
                        50 Min lernen, 10 Min Pause - gemeinsam!
                    </p>
                </div>
                <div>
                    <strong>🤝 Alle einbeziehen</strong>
                    <p style="font-size: 0.875rem; margin-top: 0.25rem;">
                        Jeder bringt Stärken mit - nutzt sie!
                    </p>
                </div>
            </div>
        </div>
        """
        st.markdown(tips_html, unsafe_allow_import streamlit as st
from datetime import datetime, time
import random
import uuid
import time as pytime

# --- Page Config ---
st.set_page_config(
    page_title="WAITT - Uni Lübeck",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS with Mobile-First Design ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Reset and Base Styles */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Root Variables */
    :root {
        --primary-gradient: linear-gradient(135deg, #A0616A 0%, #6B2C3A 100%);
        --secondary-gradient: linear-gradient(135deg, #8B5A6B, #6B2C3A);
        --card-bg: rgba(255, 255, 255, 0.95);
        --text-primary: #374151;
        --text-secondary: #6b7280;
        --accent-pink: #831843;
        --accent-light: #F9A8D4;
        --spacing-xs: 0.5rem;
        --spacing-sm: 1rem;
        --spacing-md: 1.5rem;
        --spacing-lg: 2rem;
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 20px;
        --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.08);
        --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.12);
        --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.16);
    }
    
    /* Global Styles */
    .stApp {
        background: var(--primary-gradient);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        min-height: 100vh;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu, footer, header {
        visibility: hidden;
    }
    
    /* Main Container */
    .main > div {
        max-width: 1200px;
        margin: 0 auto;
        padding: var(--spacing-sm);
    }
    
    /* Typography */
    .main-title {
        text-align: center;
        font-size: clamp(2.5rem, 8vw, 4rem);
        font-weight: 700;
        background: linear-gradient(135deg, #ffffff, #f0f0f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: var(--spacing-sm);
        letter-spacing: -0.02em;
        line-height: 1.1;
    }
    
    .subtitle {
        text-align: center;
        color: rgba(255, 255, 255, 0.9);
        font-size: clamp(1rem, 3vw, 1.3rem);
        margin-bottom: var(--spacing-lg);
        font-weight: 400;
        letter-spacing: 0.01em;
    }
    
    /* Tab Navigation */
    .stTabs {
        margin-top: var(--spacing-md);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background: rgba(255, 255, 255, 0.1);
        padding: 4px;
        border-radius: var(--radius-lg);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: var(--spacing-md);
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        scrollbar-width: none;
    }
    
    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
        display: none;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        padding: 0 var(--spacing-sm);
        background: transparent;
        border-radius: var(--radius-md);
        color: rgba(255, 255, 255, 0.8);
        font-weight: 500;
        border: none;
        transition: all 0.3s ease;
        font-size: clamp(0.75rem, 2vw, 0.875rem);
        white-space: nowrap;
        flex-shrink: 0;
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--secondary-gradient) !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(139, 90, 107, 0.3);
    }
    
    /* Cards */
    .card {
        background: var(--card-bg);
        border-radius: var(--radius-lg);
        padding: var(--spacing-md);
        margin-bottom: var(--spacing-md);
        box-shadow: var(--shadow-md);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    /* Group Cards */
    .group-card {
        position: relative;
        overflow: hidden;
        border-top: 4px solid var(--accent-pink);
    }
    
    .group-header {
        display: flex;
        align-items: flex-start;
        gap: var(--spacing-sm);
        margin-bottom: var(--spacing-md);
    }
    
    .group-icon {
        width: 50px;
        height: 50px;
        min-width: 50px;
        border-radius: var(--radius-md);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        background: var(--primary-gradient);
        color: white;
        box-shadow: var(--shadow-sm);
    }
    
    .group-content {
        flex: 1;
        min-width: 0;
    }
    
    .group-title {
        font-size: clamp(1.1rem, 3vw, 1.3rem);
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: var(--spacing-xs);
        word-break: break-word;
    }
    
    .group-meta {
        display: flex;
        flex-wrap: wrap;
        gap: var(--spacing-xs);
        margin-top: var(--spacing-sm);
    }
    
    .meta-item {
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
        background: #f3f4f6;
        padding: 0.375rem 0.75rem;
        border-radius: var(--radius-lg);
        font-size: 0.75rem;
        font-weight: 500;
        color: var(--text-secondary);
    }
    
    .spaces-badge {
        background: linear-gradient(135deg, #FDF2F8, #FCE7F3);
        color: var(--accent-pink);
        padding: 0.375rem 0.75rem;
        border-radius: var(--radius-lg);
        font-size: 0.75rem;
        font-weight: 600;
        border: 1px solid var(--accent-light);
        display: inline-block;
    }
    
    /* Question Box */
    .question-box {
        background: linear-gradient(135deg, #FDF2F8, #FCE7F3);
        padding: var(--spacing-sm);
        border-radius: var(--radius-md);
        margin: var(--spacing-sm) 0;
        border-left: 3px solid #BE185D;
    }
    
    .question-label {
        font-size: 0.625rem;
        font-weight: 600;
        color: var(--accent-pink);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.25rem;
    }
    
    .question-text {
        font-style: italic;
        color: var(--text-primary);
        font-size: clamp(0.875rem, 2.5vw, 1rem);
        line-height: 1.5;
    }
    
    /* Metrics Dashboard */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: var(--spacing-sm);
        margin-bottom: var(--spacing-lg);
    }
    
    .metric-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: var(--radius-md);
        padding: var(--spacing-sm);
        text-align: center;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }
    
    .metric-container:hover {
        background: rgba(255, 255, 255, 0.15);
        transform: translateY(-2px);
    }
    
    .metric-value {
        font-size: clamp(1.75rem, 4vw, 2.25rem);
        font-weight: 700;
        color: white;
        line-height: 1;
    }
    
    .metric-label {
        font-size: clamp(0.625rem, 2vw, 0.75rem);
        color: rgba(255, 255, 255, 0.8);
        margin-top: var(--spacing-xs);
        font-weight: 500;
        letter-spacing: 0.02em;
    }
    
    /* Forms */
    .form-container {
        background: var(--card-bg);
        border-radius: var(--radius-lg);
        padding: var(--spacing-lg);
        box-shadow: var(--shadow-lg);
    }
    
    .form-title {
        text-align: center;
        font-size: clamp(1.25rem, 4vw, 1.75rem);
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: var(--spacing-lg);
    }
    
    /* Buttons */
    .stButton > button {
        background: var(--primary-gradient);
        color: white;
        border: none;
        border-radius: var(--radius-lg);
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: var(--shadow-sm);
        min-height: 44px;
        font-size: clamp(0.875rem, 2.5vw, 1rem);
        width: 100%;
        cursor: pointer;
        touch-action: manipulation;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: var(--shadow-md);
        background: var(--secondary-gradient);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stTimeInput > div > div > input {
        border-radius: var(--radius-md);
        border: 2px solid #e5e7eb;
        padding: 0.75rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        min-height: 44px;
        width: 100%;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--accent-pink);
        box-shadow: 0 0 0 3px rgba(160, 97, 106, 0.1);
        outline: none;
    }
    
    /* Member Tags */
    .member-tag {
        background: linear-gradient(135deg, #FDF2F8, #FCE7F3);
        color: var(--accent-pink);
        padding: 0.375rem 0.75rem;
        border-radius: var(--radius-lg);
        font-size: 0.75rem;
        font-weight: 500;
        border: 1px solid var(--accent-light);
        display: inline-block;
        margin: 0.25rem;
    }
    
    /* Answer Items */
    .answer-item {
        background: #f9fafb;
        padding: var(--spacing-sm);
        border-radius: var(--radius-md);
        margin: var(--spacing-xs) 0;
        border-left: 3px solid var(--accent-pink);
    }
    
    .answer-author {
        font-weight: 600;
        color: var(--accent-pink);
        margin-bottom: 0.25rem;
        font-size: 0.875rem;
    }
    
    /* Countdown Timer */
    .countdown-container {
        background: linear-gradient(135deg, #FDF2F8, #FCE7F3);
        border-radius: var(--radius-lg);
        padding: var(--spacing-lg);
        text-align: center;
        border: 2px solid var(--accent-light);
        margin: var(--spacing-md) 0;
        box-shadow: var(--shadow-md);
    }
    
    .countdown-display {
        font-size: clamp(3rem, 12vw, 5rem);
        font-weight: bold;
        color: var(--accent-pink);
        margin: var(--spacing-md) 0;
        font-family: 'SF Mono', 'Monaco', 'Courier New', monospace;
        line-height: 1;
        text-shadow: 2px 2px 4px rgba(131, 24, 67, 0.1);
    }
    
    .countdown-text {
        font-size: clamp(0.875rem, 2.5vw, 1.1rem);
        color: #6B2C3A;
        margin: var(--spacing-sm) 0;
        font-style: italic;
        line-height: 1.6;
        max-width: 500px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Reward System */
    .reward-container {
        background: linear-gradient(135deg, #FEF3C7, #FDE68A);
        border-radius: var(--radius-lg);
        padding: var(--spacing-md);
        border: 2px solid #F59E0B;
        margin: var(--spacing-md) 0;
        box-shadow: var(--shadow-md);
    }
    
    .stamps-grid {
        display: grid;
        grid-template-columns: repeat(5, 1fr);
        gap: var(--spacing-xs);
        max-width: 300px;
        margin: var(--spacing-md) auto;
    }
    
    .stamp {
        aspect-ratio: 1;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: clamp(1rem, 3vw, 1.25rem);
        transition: all 0.3s ease;
    }
    
    .stamp-earned {
        background: linear-gradient(135deg, #10B981, #059669);
        color: white;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        animation: stampBounce 0.5s ease;
    }
    
    @keyframes stampBounce {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    
    .stamp-empty {
        background: #E5E7EB;
        color: #9CA3AF;
        border: 2px dashed #D1D5DB;
        font-size: clamp(0.625rem, 2vw, 0.875rem);
    }
    
    /* Pause Activities */
    .activity-card {
        background: white;
        border-radius: var(--radius-lg);
        padding: var(--spacing-md);
        box-shadow: var(--shadow-md);
        border-left: 4px solid var(--accent-pink);
        margin: var(--spacing-md) 0;
    }
    
    .activity-header {
        font-size: clamp(1.1rem, 3vw, 1.3rem);
        color: var(--accent-pink);
        font-weight: 600;
        margin-bottom: var(--spacing-sm);
    }
    
    .activity-meta {
        display: flex;
        flex-wrap: wrap;
        gap: var(--spacing-sm);
        margin-bottom: var(--spacing-sm);
        font-size: 0.875rem;
        color: var(--text-secondary);
    }
    
    .activity-instructions {
        background: #F9FAFB;
        padding: var(--spacing-sm);
        border-radius: var(--radius-md);
        border-left: 4px solid #A0616A;
        margin-top: var(--spacing-sm);
    }
    
    /* Pinnwand Entries */
    .pinnwand-entry {
        padding: var(--spacing-md);
        border-radius: var(--radius-md);
        margin: var(--spacing-sm) 0;
        box-shadow: var(--shadow-sm);
        position: relative;
        transition: all 0.3s ease;
        min-height: 100px;
        display: flex;
        align-items: center;
        cursor: pointer;
    }
    
    .pinnwand-entry:hover {
        transform: scale(1.02) rotate(0deg) !important;
        box-shadow: var(--shadow-md);
    }
    
    .pin-icon {
        position: absolute;
        top: -8px;
        right: 12px;
        font-size: 1.25rem;
        filter: drop-shadow(2px 2px 4px rgba(0, 0, 0, 0.1));
    }
    
    /* Responsive Adjustments */
    @media (max-width: 768px) {
        .main > div {
            padding: var(--spacing-xs);
        }
        
        .metrics-grid {
            grid-template-columns: repeat(2, 1fr);
        }
        
        .group-header {
            flex-direction: column;
        }
        
        .group-icon {
            width: 40px;
            height: 40px;
            min-width: 40px;
            font-size: 1.25rem;
        }
        
        .stamps-grid {
            max-width: 250px;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 0 var(--spacing-xs);
            font-size: 0.75rem;
        }
        
        .form-container {
            padding: var(--spacing-md);
        }
        
        /* Touch-friendly spacing */
        .stButton > button {
            margin: var(--spacing-xs) 0;
        }
        
        /* Stack columns on mobile */
        .stColumns > div {
            margin-bottom: var(--spacing-sm);
        }
    }
    
    @media (max-width: 480px) {
        .main-title {
            font-size: 2rem;
        }
        
        .metrics-grid {
            gap: var(--spacing-xs);
        }
        
        .metric-container {
            padding: var(--spacing-xs);
        }
    }
    
    /* Utility Classes */
    .text-center { text-align: center; }
    .mt-1 { margin-top: var(--spacing-sm); }
    .mt-2 { margin-top: var(--spacing-md); }
    .mb-1 { margin-bottom: var(--spacing-sm); }
    .mb-2 { margin-bottom: var(--spacing-md); }
    
    /* Animation Classes */
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Success Messages */
    .stSuccess {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1), rgba(5, 150, 105, 0.1));
        border-left: 4px solid #10B981;
        border-radius: var(--radius-md);
        padding: var(--spacing-sm);
        margin: var(--spacing-sm) 0;
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1), rgba(217, 119, 6, 0.1));
        border-left: 4px solid #F59E0B;
        border-radius: var(--radius-md);
        padding: var(--spacing-sm);
        margin: var(--spacing-sm) 0;
    }
    
    .stInfo {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(37, 99, 235, 0.1));
        border-left: 4px solid #3B82F6;
        border-radius: var(--radius-md);
        padding: var(--spacing-sm);
        margin: var(--spacing-sm) 0;
    }
    
    /* Prevent text selection on buttons */
    button {
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
    }
    
    /* Smooth scrolling */
    html {
        scroll-behavior: smooth;
    }
    
    /* Hide scrollbar but keep functionality */
    .main::-webkit-scrollbar {
        width: 8px;
    }
    
    .main::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
    }
    
    .main::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.3);
        border-radius: 4px;
    }
    
    /* Expander styling */
    .streamlit-expander {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: var(--radius-md);
        margin: var(--spacing-sm) 0;
    }
    
    /* Radio button styling */
    .stRadio > div {
        display: flex;
        flex-wrap: wrap;
        gap: var(--spacing-sm);
    }
    
    .stRadio > div > label {
        background: rgba(255, 255, 255, 0.1);
        padding: var(--spacing-xs) var(--spacing-sm);
        border-radius: var(--radius-lg);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .stRadio > div > label:hover {
        background: rgba(255, 255, 255, 0.2);
    }
    
    /* Progress bar styling */
    .stProgress > div > div {
        background: var(--primary-gradient);
        border-radius: var(--radius-lg);
    }
    
    /* Ensure clickable areas are large enough for mobile */
    a, button, input, select, textarea {
        min-height: 44px;
        min-width: 44px;
    }
    
    /* Fix overlapping issues */
    .element-container {
        margin-bottom: var(--spacing-sm) !important;
    }
    
    .stMarkdown {
        margin-bottom: var(--spacing-xs) !important;
    }
    
    /* Ensure proper z-index stacking */
    .stTabs {
        position: relative;
        z-index: 10;
    }
    
    .card {
        position: relative;
        z-index: 1;
    }
    
    /* Fix column spacing on mobile */
    @media (max-width: 768px) {
        [data-testid="column"] {
            padding: 0 var(--spacing-xs) !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- Helper Functions ---
def init_session_state():
    """Initialize all session state variables"""
    if "groups" not in st.session_state:
        st.session_state.groups = [
            {
                "id": "stats_001",
                "topic": "Statistik Klausur - Gemeinsam durchboxen",
                "time": "10:00",
                "room": "Bibliothek Gruppenraum 1",
                "max": 4,
                "members": ["Anna", "Ben"],
                "question": "Was ist deine größte Prokrastinationsgefahr beim Lernen?",
                "answers": {
                    "Anna": "Netflix-Marathons und endloses Scrollen durch Social Media",
                    "Ben": "Perfektionismus - ich bleibe zu lange an einzelnen Aufgaben hängen"
                },
                "icon": "📊",
                "category": "stats"
            },
            {
                "id": "psych_001", 
                "topic": "Klinische Psychologie - Prüfungsvorbereitung",
                "time": "14:30",
                "room": "Mensa Terrasse",
                "max": 3,
                "members": ["Chris"],
                "question": "Was motiviert dich heute am meisten zum Lernen?",
                "answers": {
                    "Chris": "Die Vorstellung, später Menschen wirklich helfen zu können"
                },
                "icon": "🧠",
                "category": "psychology"
            },
            {
                "id": "med_001",
                "topic": "Anatomie Testat - Lernmarathon",
                "time": "16:00",
                "room": "Wakenitz-Ufer (bei gutem Wetter)",
                "max": 6,
                "members": ["Lisa", "Tom", "Sarah"],
                "question": "Welche Lernmethode hilft dir am besten beim Auswendiglernen?",
                "answers": {
                    "Lisa": "Karteikarten und ständige Wiederholung",
                    "Tom": "Zusammen mit anderen laut vorsagen",
                    "Sarah": "Eselsbrücken und verrückte Geschichten erfinden"
                },
                "icon": "⚕️",
                "category": "medicine"
            },
            {
                "id": "cs_001",
                "topic": "Informatik - Algorithmen & Datenstrukturen",
                "time": "18:00",
                "room": "Online (Discord)",
                "max": 5,
                "members": ["Max", "Julia"],
                "question": "Wie gehst du mit Frustration beim Programmieren um?",
                "answers": {
                    "Max": "Erstmal aufstehen, durchatmen und einen Kaffee holen",
                    "Julia": "Rubber Duck Debugging - dem Gummienten-Kollegen alles erklären"
                },
                "icon": "💻",
                "category": "computer_science"
            }
        ]
    
    if "joined_groups" not in st.session_state:
        st.session_state.joined_groups = []
    
    if "pinnwand_entries" not in st.session_state:
        st.session_state.pinnwand_entries = [
            "Die Wakenitz-Spaziergänge zwischen den Lerneinheiten sind Gold wert! 🌊",
            "Mensa-Terrasse + Lerngruppe + Sonne = perfekte Kombi für produktives Lernen ☀️",
            "Tipp: Die Bibliothek hat neue Ruheräume - perfekt für Powernaps! 😴",
            "Nach 3 Stunden Anatomie hilft nur noch Marzipan von Niederegger 🍫",
            "Lerngruppen-Treffen am Holstentor macht Geschichte plötzlich interessant! 🏛️",
            "Gemeinsames Kochen in der WG nach dem Lernen = beste Motivation! 🍝"
        ]
    
    if "current_question" not in st.session_state:
        st.session_state.current_question = "Was hilft dir, beim Lernen nicht die Lebensfreude zu verlieren?"
    
    if "pause_statistics" not in st.session_state:
        st.session_state.pause_statistics = {
            "solo_pausen": 0,
            "gruppen_pausen": 0,
            "total_time": 0,
            "trave_spaziergaenge": 0,
            "wakenitz_besuche": 0,
            "mensa_pausen": 0,
            "meditation_minuten": 0,
            "bewegung_minuten": 0
        }
    
    if "reward_stamps" not in st.session_state:
        st.session_state.reward_stamps = 0
    
    if "reward_claimed" not in st.session_state:
        st.session_state.reward_claimed = False
    
    if "countdown_active" not in st.session_state:
        st.session_state.countdown_active = False
    
    if "countdown_time" not in st.session_state:
        st.session_state.countdown_time = 120
    
    if "countdown_start" not in st.session_state:
        st.session_state.countdown_start = None
    
    if "current_solo_activity" not in st.session_state:
        st.session_state.current_solo_activity = None
    
    if "current_group_activity" not in st.session_state:
        st.session_state.current_group_activity = None
    
    if "pause_history" not in st.session_state:
        st.session_state.pause_history = []

def get_group_card_class(category):
    """Get CSS class for group card based on category"""
    classes = {
        "stats": "#A0616A",
        "psychology": "#C4626D", 
        "bio": "#B85450",
        "medicine": "#D97706",
        "computer_science": "#3B82F6",
        "other": "#8B5A6B"
    }
    return classes.get(category, "#8B5A6B")

def show_success_message(message):
    """Display success message"""
    st.success(f"✅ {message}")

def show_warning_message(message):
    """Display warning message"""
    st.warning(f"⚠️ {message}")

def show_info_message(message):
    """Display info message"""
    st.info(f"ℹ️ {message}")

def add_reward_stamp(activity_type="general"):
    """Add a stamp to the reward system"""
    if st.session_state.reward_stamps < 10:
        st.session_state.reward_stamps += 1
        
        # Track activity in history
        st.session_state.pause_history.append({
            "type": activity_type,
            "timestamp": datetime.now(),
            "stamps_earned": 1
        })
        
        if st.session_state.reward_stamps >= 10 and not st.session_state.reward_claimed:
            st.balloons()
            show_success_message("🎉 Glückwunsch! Du hast 10 Stempel gesammelt! Zeige diese App in der Mensa vor und erhalte ein kostenloses Essen!")
            st.session_state.reward_claimed = True
        else:
            remaining = 10 - st.session_state.reward_stamps
            encouragements = [
                f"Super! Noch {remaining} Stempel bis zum kostenlosen Mensa-Essen! 🍽️",
                f"Weiter so! Nur noch {remaining} Stempel! 💪",
                f"Toll gemacht! {remaining} Stempel fehlen noch! 🌟",
                f"Du bist auf dem richtigen Weg! Noch {remaining} Stempel! 🎯"
            ]
            show_success_message(random.choice(encouragements))

def render_group_card(group):
    """Render a group card with improved mobile design"""
    color = get_group_card_class(group.get("category", "other"))
    free_spaces = group["max"] - len(group["members"])
    is_joined = group["id"] in st.session_state.joined_groups
    
    card_html = f"""
    <div class="card group-card fade-in" style="border-top-color: {color};">
        <div class="group-header">
            <div class="group-icon">{group["icon"]}</div>
            <div class="group-content">
                <h3 class="group-title">{group["topic"]}</h3>
                <span class="spaces-badge">{'Voll' if free_spaces == 0 else f'{free_spaces} freie Plätze'}</span>
            </div>
        </div>
        <div class="group-meta">
            <div class="meta-item">🕐 {group["time"]}</div>
            <div class="meta-item">📍 {group["room"]}</div>
            <div class="meta-item">👥 {len(group["members"])}/{group["max"]}</div>
        </div>
        <div class="question-box">
            <div class="question-label">Einstiegsfrage</div>
            <div class="question-text">"{group["question"]}"</div>
        </div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)
    
    return is_joined, free_spaces

def render_reward_system():
    """Render the stamp reward system with visual feedback"""
    stamps = st.session_state.reward_stamps
    
    reward_html = f"""
    <div class="reward-container fade-in">
        <h4 style="color: #92400e; margin-bottom: 1rem; text-align: center;">
            🏆 Mensa-Belohnungssystem
        </h4>
        <p style="color: #78350f; text-align: center; margin-bottom: 1rem; font-size: 0.9rem;">
            Sammle 10 Stempel für ein kostenloses Mensa-Essen!<br>
            <strong>Jede Pause, jede Gruppenaktivität zählt! 💪</strong>
        </p>
    </div>
    """
    st.markdown(reward_html, unsafe_allow_html=True)
    
    # Render stamp grid
    stamps_html = '<div class="stamps-grid">'
    for i in range(10):
        if i < stamps:
            stamps_html += '<div class="stamp stamp-earned">⭐</div>'
        else:
            stamps_html += f'<div class="stamp stamp-empty">{i+1}</div>'
    stamps_html += '</div>'
    
    st.markdown(stamps_html, unsafe_allow_html=True)
    
    # Show progress
    progress = stamps / 10
    st.progress(progress)
    
    if stamps >= 10 and not st.session_state.reward_claimed:
        claim_html = """
        <div style="background: linear-gradient(135deg, #10B981, #059669); color: white; 
             padding: 1.5rem; border-radius: 12px; text-align: center; margin: 1rem 0;">
            <h4 style="margin-bottom: 1rem; color: white;">🎉 BELOHNUNG BEREIT! 🎉</h4>
            <p style="margin-bottom: 0.5rem;">Zeige diese Seite in der Mensa vor!</p>
            <p style="margin: 0; font-weight: 600;">
                📍 Mensa Uni Lübeck<br>
                Mönkhofer Weg 241, 23562 Lübeck
            </p>
        </div>
        """
        st.markdown(claim_html, unsafe_allow_html=True)
        
        if st.button("✅ Belohnung eingelöst", use_container_width=True):
            st.session_state.reward_claimed = True
            st.session_state.reward_stamps = 0
            show_success_message("Belohnung eingelöst! Du kannst wieder neue Stempel sammeln. 🎯")
            st.rerun()
    
    elif stamps < 10:
        remaining = 10 - stamps
        tips = [
            "💡 Tipp: Jede 2-Minuten-Pause bringt einen Stempel!",
            "💡 Tipp: Gruppenaktivitäten geben oft 2 Stempel!",
            "💡 Tipp: Auch Pinnwand-Beiträge werden belohnt!",
            "💡 Tipp: Outdoor-Pausen an der Wakenitz sind besonders wertvoll!"
        ]
        st.write(f"**Noch {remaining} Stempel bis zur Belohnung!**")
        st.write(random.choice(tips))

def render_countdown_timer():
    """Render 2-minute countdown timer with motivational messages"""
    if not st.session_state.countdown_active:
        intro_html = """
        <div class="countdown-container">
            <h3 style="color: #831843; margin-bottom: 1rem;">🧘 Die 2-Minuten-Nichtstun-Challenge</h3>
            <p style="color: #6B2C3A; margin-bottom: 1.5rem; line-height: 1.6;">
                <strong>Wann hast du das letzte Mal wirklich NICHTS getan?</strong><br>
                Keine Ablenkung. Kein Handy. Keine Gedanken ans Lernen.<br>
                Nur du und 2 Minuten pure Entspannung. 🌸
            </p>
            <p style="font-size: 0.9rem; color: #9D174D;">
                Diese Übung hilft dir, mental herunterzufahren und neue Energie zu tanken.
            </p>
        </div>
        """
        st.markdown(intro_html, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🎯 Challenge starten", use_container_width=True):
                st.session_state.countdown_active = True
                st.session_state.countdown_time = 120
                st.session_state.countdown_start = pytime.time()
                st.rerun()
    
    else:
        # Calculate remaining time
        if st.session_state.countdown_start:
            elapsed = pytime.time() - st.session_state.countdown_start
            remaining = max(0, 120 - int(elapsed))
            st.session_state.countdown_time = remaining
        else:
            remaining = st.session_state.countdown_time
        
        if remaining > 0:
            minutes = remaining // 60
            seconds = remaining % 60
            
            # Motivational messages based on time
            if remaining > 90:
                message = "Lass los... Atme tief ein und aus... 🌊"
            elif remaining > 60:
                message = "Du machst das großartig! Bleib dabei... 🌟"
            elif remaining > 30:
                message = "Spüre, wie die Ruhe sich ausbreitet... 🍃"
            else:
                message = "Fast geschafft! Du bist stärker als du denkst! 💪"
            
            timer_html = f"""
            <div class="countdown-container">
                <div class="countdown-display">{minutes:02d}:{seconds:02d}</div>
                <div class="countdown-text">
                    {message}<br>
                    <span style="font-size: 0.85rem; opacity: 0.8;">
                        Fokussiere dich auf deinen Atem... Ein... Aus...
                    </span>
                </div>
            </div>
            """
            st.markdown(timer_html, unsafe_allow_html=True)
            
            # Control buttons
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("⏸️ Pausieren", use_container_width=True):
                    st.session_state.countdown_active = False
                    st.session_state.countdown_start = None
                    st.rerun()
            with col2:
                if st.button("🔄 Neustart", use_container_width=True):
                    st.session_state.countdown_time = 120
                    st.session_state.countdown_start = pytime.time()
                    st.rerun()
            with col3:
                if st.button("⏭️ Beenden", use_container_width=True):
                    st.session_state.countdown_time = 0
                    st.rerun()
            
            # Auto-refresh for countdown
            if remaining > 0:
                pytime.sleep(1)
                st.rerun()
        
        else:
            # Challenge completed
            complete_html = """
            <div class="countdown-container" style="background: linear-gradient(135deg, #D1FAE5, #A7F3D0);">
                <div style="font-size: 3rem; margin: 1rem 0;">🎉</div>
                <h3 style="color: #065F46; margin-bottom: 1rem;">Geschafft!</h3>
                <p style="color: #047857; line-height: 1.6; margin-bottom: 1.5rem;">
                    <strong>Du hast es geschafft, 2 Minuten nur für dich zu sein!</strong><br>
                    Das war ein wichtiger Schritt für deine mentale Gesundheit. 💚<br>
                    <span style="font-size: 0.9rem;">
                        Studien zeigen: Regelmäßige Mikropausen steigern die Konzentration um bis zu 40%!
                    </span>
                </p>
            </div>
            """
            st.markdown(complete_html, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Pause abschließen", use_container_width=True):
                    st.session_state.countdown_active = False
                    st.session_state.countdown_start = None
                    st.session_state.pause_statistics["solo_pausen"] += 1
                    st.session_state.pause_statistics["meditation_minuten"] += 2
                    st.session_state.pause_statistics["total_time"] += 2
                    add_reward_stamp("meditation")
                    st.rerun()
            
            with col2:
                if st.button("🔄 Nochmal 2 Minuten", use_container_width=True):
                    st.session_state.countdown_time = 120
                    st.session_state.countdown_start = pytime.time()
                    st.rerun()

def get_luebeck_activities():
    """Get activities specifically for Lübeck students"""
    return {
        "solo": [
            {
                "name": "Wakenitz-Meditation 🦆",
                "duration": "10 min",
                "type": "Natur & Achtsamkeit",
                "location": "Wakenitz-Ufer (5 Min. vom Campus)",
                "description": "Entspannung am 'Amazonas des Nordens'",
                "instructions": """
                1. Gehe zum Wakenitz-Ufer (vom Campus Richtung Drägerpark)
                2. Suche dir einen ruhigen Platz am Wasser
                3. Beobachte 5 Minuten lang nur das Wasser und die Enten
                4. Atme dabei bewusst tief ein und aus
                5. Lass alle Gedanken ans Lernen los
                """,
                "benefits": "Reduziert Stress, verbessert Konzentration",
                "stamps": 1
            },
            {
                "name": "Trave-Power-Walk 🚶‍♀️",
                "duration": "15 min",
                "type": "Bewegung & Frischluft",
                "location": "Trave-Promenade",
                "description": "Aktive Pause mit Aussicht auf die Altstadt",
                "instructions": """
                1. Starte an der Puppenbrücke beim Holstentor
                2. Gehe zügig (aber nicht joggen!) entlang der Trave
                3. Konzentriere dich auf deine Schritte und Atmung
                4. Genieße die Aussicht auf die Altstadtsilhouette
                5. Kehre über die Hubbrücke zurück
                """,
                "benefits": "Aktiviert Kreislauf, klärt Gedanken",
                "stamps": 1
            },
            {
                "name": "Mensa-Terrassen-Yoga 🧘",
                "duration": "5 min",
                "type": "Schnelle Erholung",
                "location": "Mensa-Dachterrasse",
                "description": "Mini-Yoga zwischen den Vorlesungen",
                "instructions": """
                1. Gehe auf die Mensa-Terrasse (auch bei kaltem Wetter!)
                2. Stelle dich aufrecht hin, Füße hüftbreit
                3. 3x Sonnengruß oder einfache Dehnübungen
                4. Beende mit 1 Minute stiller Beobachtung der Umgebung
                """,
                "benefits": "Lockert Verspannungen, erfrischt",
                "stamps": 1
            },
            {
                "name": "Holstentor-Achtsamkeit 🏛️",
                "duration": "8 min",
                "type": "Kultur & Besinnung",
                "location": "Holstentor / Holstentorplatz",
                "description": "Historische Auszeit vom Uni-Stress",
                "instructions": """
                1. Fahre/gehe zum Holstentor (10 Min. mit Rad vom Campus)
                2. Setze dich auf eine Bank mit Blick aufs Tor
                3. Stelle dir vor, wie viele Studierende hier schon saßen
                4. Lass den Moment auf dich wirken
                5. Mache 3 Fotos aus ungewöhnlichen Perspektiven
                """,
                "benefits": "Perspektivwechsel, Entschleunigung",
                "stamps": 1
            },
            {
                "name": "Bibliotheks-Stretching 📚",
                "duration": "3 min",
                "type": "Mikropause",
                "location": "Überall (Bibliothek, Hörsaal)",
                "description": "Unauffällige Übungen für zwischendurch",
                "instructions": """
                1. Schulterkreisen: 10x vorwärts, 10x rückwärts
                2. Nacken dehnen: Kopf sanft zur Seite neigen
                3. Handgelenke kreisen (wichtig beim Schreiben!)
                4. Füße unter dem Tisch kreisen
                5. Tief durchatmen und lächeln :)
                """,
                "benefits": "Beugt Verspannungen vor",
                "stamps": 1
            }
        ],
        "gruppe": [
            {
                "name": "Wakenitz-Picknick 🧺",
                "duration": "45 min",
                "type": "Soziales & Natur",
                "location": "Wakenitz-Wiesen beim Drägerpark",
                "description": "Gemeinsame Auszeit mit Snacks und Spielen",
                "instructions": """
                VORBEREITUNG:
                - Jeder bringt einen Snack mit (Obst, Nüsse, Kekse)
                - Decke oder Isomatten mitbringen
                - Optional: Frisbee, Kartenspiel
                
                ABLAUF:
                1. Trefft euch am Campus und radelt gemeinsam zur Wakenitz
                2. Erste 10 Min: Handys in eine Tasche - Digital Detox!
                3. Reihum erzählt jeder eine positive Sache vom Tag
                4. Gemeinsam essen und dabei NICHT über Uni reden
                5. Abschluss: 5 Min gemeinsame Stille genießen
                """,
                "gruppendynamik": "Stärkt Zusammenhalt, reduziert Einsamkeit",
                "stamps": 2
            },
            {
                "name": "Altstadt-Rallye 🗺️",
                "duration": "60 min",
                "type": "Bewegung & Entdeckung",
                "location": "Lübecker Altstadt",
                "description": "Spielerische Erkundungstour in Kleingruppen",
                "instructions": """
                SPIELREGELN:
                - Teilt euch in 2er-Teams auf
                - Jedes Team bekommt 3 Aufgaben (siehe unten)
                - Treffpunkt nach 45 Min am Niederegger
                
                AUFGABEN-BEISPIELE:
                1. Findet den schmalsten Gang der Stadt (Foto als Beweis)
                2. Zählt die Türme, die ihr vom Koberg aus seht
                3. Entdeckt ein verstecktes Café und fragt nach der Spezialität
                4. Findet heraus, was ein "Lübecker Rotspon" ist
                5. Macht ein kreatives Gruppenfoto vor dem Buddenbrookhaus
                
                ABSCHLUSS: Gemeinsam Marzipan probieren!
                """,
                "gruppendynamik": "Fördert Teamwork und Kommunikation",
                "stamps": 2
            },
            {
                "name": "Mensa-Talk-Runde ☕",
                "duration": "30 min",
                "type": "Soziale Verbindung",
                "location": "Mensa Café",
                "description": "Strukturiertes Kennenlernen bei Kaffee",
                "instructions": """
                GESPRÄCHSTHEMEN (je 5 Min):
                1. "Mein peinlichster Uni-Moment" - Lachen garantiert!
                2. "Was ich nach dem Studium wirklich machen will"
                3. "Meine beste Prokrastinations-Geschichte"
                4. "Ein Ort in Lübeck, den nicht jeder kennt"
                5. "Was ich gerne vor dem Studium gewusst hätte"
                
                REGEL: Jeder kommt zu Wort, aktives Zuhören!
                BONUS: Wer die beste Geschichte hat, bekommt einen Kaffee spendiert
                """,
                "gruppendynamik": "Baut Vertrauen auf, reduziert Isolation",
                "stamps": 2
            },
            {
                "name": "Falkenwiese-Olympics 🏃",
                "duration": "40 min",
                "type": "Sport & Spaß",
                "location": "Sportzentrum Falkenwiese",
                "description": "Lustige Mini-Wettkämpfe ohne Leistungsdruck",
                "instructions": """
                DISZIPLINEN (je 5-10 Min):
                1. Frisbee-Zielwerfen (auf Bäume/Mülleimer)
                2. Balancier-Wettbewerb auf der Slackline
                3. Gruppen-Jonglage (mit allem was da ist)
                4. "Zeitlupen-Rennen" (wer am langsamsten ist, gewinnt!)
                5. Wikingerschach oder Boule (wenn vorhanden)
                
                WICHTIG: Es geht um Spaß, nicht um Gewinnen!
                ABSCHLUSS: Gemeinsam auf der Wiese liegen und Wolken deuten
                """,
                "gruppendynamik": "Löst Anspannung, fördert Lachen",
                "stamps": 2
            },
            {
                "name": "Trave-Gesprächsspaziergang 💬",
                "duration": "25 min",
                "type": "Walk & Talk",
                "location": "Entlang der Trave",
                "description": "Bewegte Gespräche in 2er-Gruppen",
                "instructions": """
                ABLAUF:
                1. Paare bilden (am besten mit jemandem, den man weniger kennt)
                2. Gemeinsam an der Trave entlang spazieren
                3. Gesprächsthema: "Was beschäftigt dich gerade wirklich?"
                
                REGELN:
                - Beide Seiten kommen gleichberechtigt zu Wort
                - Keine Ratschläge geben, nur zuhören und nachfragen
                - Was besprochen wird, bleibt unter euch
                
                NACH 15 MIN: Partnerwechsel für den Rückweg
                """,
                "gruppendynamik": "Schafft tiefe Verbindungen",
                "stamps": 2
            }
        ]
    }

def get_luebeck_locations():
    """Get list of meeting locations in Lübeck"""
    return [
        "📚 Bibliothek Gruppenraum 1",
        "📚 Bibliothek Gruppenraum 2", 
        "📚 Bibliothek Stille Etage",
        "☕ Mensa Terrasse",
        "☕ Café Campus",
        "🌳 Lernwiese (bei gutem Wetter)",
        "🌊 Wakenitz-Ufer beim Drägerpark",
        "🌊 Trave-Promenade",
        "☕ Café Affenbrot (Altstadt)",
        "☕ BÄCKEREI Junge am Koberg",
        "🏛️ St. Annen-Museum Café",
        "🌳 Schulgarten Lübeck",
        "🏃 Sportzentrum Falkenwiese",
        "💻 Online (Zoom/Discord)",
        "🏠 Wohnheim Gemeinschaftsraum"
    ]

def render_pause_activity_card(activity, activity_type="solo"):
    """Render a pause activity card with all details"""
    emoji_map = {
        "Natur & Achtsamkeit": "🌿",
        "Bewegung & Frischluft": "🏃",
        "Bewegung": "🏃",
        "Schnelle Erholung": "⚡",
        "Kultur & Besinnung": "🏛️",
        "Mikropause": "⏱️",
        "Soziales & Natur": "👥",
        "Bewegung & Entdeckung": "🗺️",
        "Soziale Verbindung": "💬",
        "Sport & Spaß": "⚽",
        "Walk & Talk": "🚶"
    }
    
    type_emoji = emoji_map.get(activity["type"], "🌟")
    
    card_html = f"""
    <div class="activity-card fade-in">
        <h3 class="activity-header">{type_emoji} {activity["name"]}</h3>
        <div class="activity-meta">
            <span>📍 {activity["location"]}</span>
            <span>⏱️ {activity["duration"]}</span>
            <span>⭐ +{activity["stamps"]} Stempel</span>
        </div>
        <p style="margin: 1rem 0; color: #4B5563;">
            <strong>{activity["description"]}</strong>
        </p>
        <div class="activity-instructions">
            <h4 style="color: #374151; margin-bottom: 0.5rem;">📝 So geht's:</h4>
            <div style="white-space: pre-line; color: #4B5563; font-size: 0.9rem;">
{activity["instructions"]}
            </div>
        </div>
        <p style="margin-top: 1rem; font-size: 0.875rem; color: #059669;">
            <strong>✨ Nutzen:</strong> {activity.get("benefits", activity.get("gruppendynamik", "Hilft dir, zu entspannen und neue Energie zu tanken"))}
        </p>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)

# --- Main App ---
def main():
    init_session_state()
    
    # Header
    st.markdown('<h1 class="main-title">WAITT</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">We\'re All In This Together - Uni Lübeck</p>', unsafe_allow_html=True)
    
    # Metrics Dashboard
    st.markdown('<div class="metrics-grid">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{len(st.session_state.groups)}</div>
            <div class="metric-label">Aktive Gruppen</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_members = sum(len(group["members"]) for group in st.session_state.groups)
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{total_members}</div>
            <div class="metric-label">Studierende vernetzt</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_pauses = st.session_state.pause_statistics["solo_pausen"] + st.session_state.pause_statistics["gruppen_pausen"]
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{total_pauses}</div>
            <div class="metric-label">Pausen genommen</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        stamps = st.session_state.reward_stamps
        stamp_emoji = "🏆" if stamps >= 10 else "⭐"
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-value">{stamps}{stamp_emoji}</div>
            <div class="metric-label">Mensa-Stempel</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Show reward system prominently when close to goal
    if st.session_state.reward_stamps >= 7:
        st.markdown("---")
        render_reward_system()
    
    # Main Navigation Tabs
    tabs = st.tabs([
        "🌿 Pausengestaltung",
        "🔍 Gruppen finden", 
        "➕ Gruppe erstellen", 
        "👥 Meine Gruppen", 
        "📌 Community-Pinnwand"
    ])
    
    # Tab
