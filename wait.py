import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Calendar } from "@/components/ui/calendar";
import { useState } from "react";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectTrigger, SelectContent, SelectItem } from "@/components/ui/select";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Dialog, DialogTrigger, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Badge } from "@/components/ui/badge";

export default function StudyGroupApp() {
  const [date, setDate] = useState<Date | undefined>(new Date());
  const [questionAnswer, setQuestionAnswer] = useState("");
  const [joinedGroups, setJoinedGroups] = useState<any[]>([]);
  const [groupMessages, setGroupMessages] = useState<{ [key: string]: string[] }>({});
  const [newMessage, setNewMessage] = useState<{ [key: string]: string }>({});
  const [weeklyAnswer, setWeeklyAnswer] = useState("");
  const [submittedWeeklyAnswers, setSubmittedWeeklyAnswers] = useState<string[]>([
    "Ich will mein Studium wirklich gut abschließen.",
    "Mein Ziel ist der Masterplatz – das treibt mich an.",
    "Ich lerne mit Freund:innen, das macht es leichter.",
    "Ich will beim nächsten Test besser abschneiden.",
    "Wenn ich heute lerne, kann ich mir morgen frei nehmen.",
    "Ich möchte mir selbst beweisen, dass ich das kann.",
    "Die Deadline rückt näher.",
    "Ich möchte nicht wieder alles auf den letzten Drücker machen."
  ]);

  const [groups, setGroups] = useState<any[]>([
    {
      id: 1,
      thema: "Statistik 1",
      groesse: "3/5",
      zeit: "25. Juni, 14:00 Uhr",
      ort: "Seminarraum A",
      frage: "Was machst du am liebsten in der Lernpause?",
      antworten: [
        "Kaffee holen und spazieren",
        "Meditation oder Musik hören",
        "Kurz TikTok checken"
      ]
    },
    {
      id: 2,
      thema: "Allgemeine Psychologie: Aufmerksamkeit",
      groesse: "2/3",
      zeit: "26. Juni, 10:00 Uhr",
      ort: "Bibliothek 1. OG",
      frage: "Wie motivierst du dich an anstrengenden Tagen?",
      antworten: ["Ich belohne mich mit Serien", "Ich erinnere mich an meine Ziele"]
    },
    {
      id: 3,
      thema: "Biopsychologie Prüfungsvorbereitung",
      groesse: "1/4",
      zeit: "27. Juni, 16:00 Uhr",
      ort: "Hörsaal 3",
      frage: "Was ist dein Lern-Life-Hack?",
      antworten: ["Pomodoro-Timer", "Mit Karteikarten abfragen"]
    }
  ]);

  const [newGroup, setNewGroup] = useState<any>({ thema: "", beschreibung: "", groesse: "", ort: "", zeit: "", datum: new Date() });

  const handleJoinGroup = (group: any, answer: string) => {
    const updatedGroup = {
      ...group,
      antworten: [...group.antworten, answer]
    };
    setJoinedGroups([...joinedGroups, updatedGroup]);
    setGroups(groups.map(g => g.id === group.id ? updatedGroup : g));
    setQuestionAnswer("");
  };

  const handleSendMessage = (groupId: number) => {
    const message = newMessage[groupId];
    if (!message) return;
    setGroupMessages(prev => ({
      ...prev,
      [groupId]: [...(prev[groupId] || []), message]
    }));
    setNewMessage(prev => ({ ...prev, [groupId]: "" }));
  };

  const handleCreateGroup = () => {
    const id = Date.now();
    const newEntry = {
      id,
      thema: newGroup.thema,
      beschreibung: newGroup.beschreibung,
      groesse: newGroup.groesse,
      zeit: newGroup.zeit,
      ort: newGroup.ort,
      datum: newGroup.datum,
      frage: "Was ist dein bestes Lern-Life-Hack?",
      antworten: []
    };
    setGroups([...groups, newEntry]);
    setNewGroup({ thema: "", beschreibung: "", groesse: "", ort: "", zeit: "", datum: new Date() });
  };

  return (
    <div className="p-4 max-w-2xl mx-auto space-y-4">
      <h1 className="text-2xl font-bold text-center">Campus Lerngruppen App</h1>

      <Tabs defaultValue="create">
        <TabsList className="grid grid-cols-3 mb-4">
          <TabsTrigger value="create">Lerngruppe erstellen</TabsTrigger>
          <TabsTrigger value="browse">Lerngruppen finden</TabsTrigger>
          <TabsTrigger value="pinnwand">Pinnwand</TabsTrigger>
        </TabsList>

        <TabsContent value="create">
          <Card>
            <CardContent className="space-y-3 p-4">
              <h2 className="text-xl font-semibold">Neue Lerngruppe erstellen</h2>
              <Input placeholder="Thema" value={newGroup.thema} onChange={e => setNewGroup({ ...newGroup, thema: e.target.value })} />
              <Textarea placeholder="Beschreibung" value={newGroup.beschreibung} onChange={e => setNewGroup({ ...newGroup, beschreibung: e.target.value })} />
              <Input placeholder="Größe (z.B. 3/5)" value={newGroup.groesse} onChange={e => setNewGroup({ ...newGroup, groesse: e.target.value })} />
              <Input placeholder="Ort (z.B. Seminarraum A)" value={newGroup.ort} onChange={e => setNewGroup({ ...newGroup, ort: e.target.value })} />
              <Input placeholder="Zeit (z.B. 14:00 Uhr)" value={newGroup.zeit} onChange={e => setNewGroup({ ...newGroup, zeit: e.target.value })} />
              <Calendar mode="single" selected={newGroup.datum} onSelect={(d) => setNewGroup({ ...newGroup, datum: d })} />
              <Button className="w-full" onClick={handleCreateGroup}>Gruppe erstellen</Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="browse">
          <Card>
            <CardContent className="p-4 space-y-3">
              <h2 className="text-xl font-semibold">Offene Lerngruppen</h2>
              {groups.map(group => (
                <Card key={group.id} className="bg-gray-50">
                  <CardContent className="p-3">
                    <p><strong>Thema:</strong> {group.thema}</p>
                    <p><strong>Größe:</strong> {group.groesse}</p>
                    <p><strong>Zeit:</strong> {group.zeit}</p>
                    <p><strong>Ort:</strong> {group.ort}</p>

                    {!joinedGroups.find(g => g.id === group.id) ? (
                      <Dialog>
                        <DialogTrigger asChild>
                          <Button className="mt-2 w-full" variant="secondary">Beitreten</Button>
                        </DialogTrigger>
                        <DialogContent>
                          <DialogHeader>
                            <DialogTitle>Frage zum Einstieg</DialogTitle>
                          </DialogHeader>
                          <p>{group.frage}</p>
                          <Textarea
                            placeholder="Antwort hier eingeben..."
                            value={questionAnswer}
                            onChange={(e) => setQuestionAnswer(e.target.value)}
                          />
                          <Button
                            disabled={!questionAnswer}
                            onClick={() => handleJoinGroup(group, questionAnswer)}
                          >
                            Antwort absenden & beitreten
                          </Button>
                        </DialogContent>
                      </Dialog>
                    ) : (
                      <div className="mt-2 text-sm bg-white border rounded p-2">
                        <p><strong>Antworten anderer:</strong></p>
                        <ul className="list-disc list-inside">
                          {group.antworten.map((a, i) => <li key={i}>{a}</li>)}
                        </ul>
                      </div>
                    )}
                  </CardContent>
                </Card>
              ))}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="pinnwand">
          <Card>
            <CardContent className="p-4 space-y-3">
              <h2 className="text-xl font-semibold">Frage der Woche</h2>
              <p className="italic">Was motiviert dich aktuell am meisten beim Lernen?</p>
              <Textarea placeholder="Anonym antworten..." value={weeklyAnswer} onChange={e => setWeeklyAnswer(e.target.value)} />
              <Button className="w-full" onClick={() => {
                if (weeklyAnswer.trim()) {
                  setSubmittedWeeklyAnswers([weeklyAnswer, ...submittedWeeklyAnswers]);
                  setWeeklyAnswer("");
                }
              }}>Antwort absenden</Button>

              <div className="mt-6">
                <h3 className="text-md font-semibold mb-2">Antworten anderer (Post-Its)</h3>
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                  {submittedWeeklyAnswers.map((answer, i) => (
                    <div
                      key={i}
                      className="rounded shadow p-3 text-sm whitespace-pre-wrap border w-full h-32 flex items-center justify-center text-center"
                      style={{
                        backgroundColor: ["#fff9b1", "#fff6a2", "#fff1a8"][i % 3],
                        fontFamily: "'Patrick Hand', cursive",
                        transform: `rotate(${(i % 2 === 0 ? 1 : -1) * (1 + Math.random())}deg)`
                      }}
                    >
                      {answer}
                    </div>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
