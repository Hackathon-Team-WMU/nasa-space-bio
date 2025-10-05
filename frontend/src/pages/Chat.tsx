import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";
import { MessageSquare, Send, Plus, Rocket, LogOut, User, Sparkles } from "lucide-react";
import { useAuth } from "@/hooks/useAuth";
import { useNavigate } from "react-router-dom";
import { supabase } from "@/integrations/supabase/client";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
}

interface ChatSession {
  id: string;
  title: string;
  messages: Message[];
  createdAt: number;
}

interface Profile {
  full_name: string | null;
  email: string;
}

const INITIAL_MESSAGE: Message = {
  id: "1",
  role: "assistant",
  content: "Hello! I'm your NASA BioExplorer assistant. Ask me anything about space biology research and experiments!",
};

const Chat = () => {
  const { user, loading, signOut } = useAuth();
  const navigate = useNavigate();
  const [profile, setProfile] = useState<Profile | null>(null);
  const [chats, setChats] = useState<ChatSession[]>([]);
  const [currentChatId, setCurrentChatId] = useState<string | null>(null);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const currentChat = chats.find((chat) => chat.id === currentChatId);
  const messages = currentChat?.messages || [INITIAL_MESSAGE];

  const suggestedPrompts = [
    "Find publications on microgravity effects on bone density",
    "Summarize the article about plant growth experiments on the ISS",
  ];

  const isEmptyChat = messages.length === 1 && messages[0].role === "assistant";

  // Redirect if not logged in
  useEffect(() => {
    if (!loading && !user) {
      navigate("/auth");
    }
  }, [user, loading, navigate]);

  // Load chats from localStorage
  useEffect(() => {
    try {
      const savedChats = localStorage.getItem("nasa_chats");
      if (savedChats) {
        const chatsData = JSON.parse(savedChats);
        setChats(chatsData);
        // Load the most recent chat
        if (chatsData.length > 0) {
          setCurrentChatId(chatsData[0].id);
        }
      }
    } catch (error) {
      console.error("Error loading chats:", error);
      // Clear corrupted data
      localStorage.removeItem("nasa_chats");
    }
  }, []);

  // Save chats to localStorage whenever they change
  useEffect(() => {
    try {
      if (chats.length > 0) {
        localStorage.setItem("nasa_chats", JSON.stringify(chats));
      }
    } catch (error) {
      console.error("Error saving chats:", error);
      // Handle storage quota exceeded
      if (error instanceof DOMException && error.name === "QuotaExceededError") {
        alert("Storage limit exceeded. Please clear some old chats.");
      }
    }
  }, [chats]);

  // Fetch user profile
  useEffect(() => {
    const fetchProfile = async () => {
      if (!user) return;

      const { data } = await supabase
        .from("profiles")
        .select("*")
        .eq("id", user.id)
        .single();

      if (data) {
        setProfile(data);
      }
    };

    fetchProfile();
  }, [user]);

  const createNewChat = () => {
    const newChat: ChatSession = {
      id: Date.now().toString(),
      title: "New Chat",
      messages: [INITIAL_MESSAGE],
      createdAt: Date.now(),
    };
    setChats((prev) => [newChat, ...prev]);
    setCurrentChatId(newChat.id);
  };

  const switchChat = (chatId: string) => {
    setCurrentChatId(chatId);
  };

  const updateChatMessages = (chatId: string, newMessages: Message[]) => {
    setChats((prev) =>
      prev.map((chat) => {
        if (chat.id === chatId) {
          // Update title based on first user message if it's still "New Chat"
          let title = chat.title;
          if (title === "New Chat") {
            const firstUserMessage = newMessages.find((msg) => msg.role === "user");
            if (firstUserMessage) {
              title = firstUserMessage.content.slice(0, 40) + (firstUserMessage.content.length > 40 ? "..." : "");
            }
          }
          return { ...chat, messages: newMessages, title };
        }
        return chat;
      })
    );
  };

  const handleSend = async (messageText?: string) => {
    const textToSend = messageText || input;
    if (!textToSend.trim() || isLoading) return;

    // Create a new chat if none exists
    let activeChatId = currentChatId;
    if (!activeChatId) {
      const newChat: ChatSession = {
        id: Date.now().toString(),
        title: "New Chat",
        messages: [INITIAL_MESSAGE],
        createdAt: Date.now(),
      };
      setChats([newChat]);
      setCurrentChatId(newChat.id);
      activeChatId = newChat.id;
    }

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: textToSend,
    };

    const currentMessages = currentChat?.messages || [INITIAL_MESSAGE];
    const updatedMessages = [...currentMessages, userMessage];
    updateChatMessages(activeChatId, updatedMessages);
    
    const queryText = textToSend;
    setInput("");
    setIsLoading(true);

    try {
      // Call Flask backend API
      const response = await fetch("http://localhost:2121/api/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: queryText }),
      });

      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }

      const data = await response.json();

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: data.response,
      };
      const finalMessages = [...updatedMessages, assistantMessage];
      updateChatMessages(activeChatId!, finalMessages);
    } catch (error) {
      console.error("Error calling API:", error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "Sorry, I encountered an error while processing your request. Please make sure the backend is running on port 2121.",
      };
      const finalMessages = [...updatedMessages, errorMessage];
      updateChatMessages(activeChatId!, finalMessages);
    } finally {
      setIsLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center bg-background">
        <div className="text-center">
          <Rocket className="w-12 h-12 text-primary animate-pulse mx-auto mb-4" />
          <p className="text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-background">
      {/* Sidebar */}
      <div className="w-64 bg-sidebar border-r border-sidebar-border flex flex-col">
        <div className="p-4">
          <div className="flex items-center gap-2 mb-6">
            <Rocket className="w-6 h-6 text-primary" />
            <span className="font-bold text-lg">BioExplorer</span>
          </div>

          <Button 
            className="mb-4 bg-primary hover:bg-primary/90 w-full"
            onClick={createNewChat}
          >
            <Plus className="w-4 h-4 mr-2" />
            New Chat
          </Button>
        </div>

        <ScrollArea className="flex-1 px-4">
          <div className="space-y-2">
            {chats.length === 0 ? (
              <p className="text-sm text-muted-foreground text-center py-4">
                No chats yet. Start a new one!
              </p>
            ) : (
              chats.map((chat) => (
                <Card
                  key={chat.id}
                  className={`p-3 border-sidebar-border hover:bg-sidebar-accent/80 cursor-pointer transition-colors ${
                    chat.id === currentChatId
                      ? "bg-sidebar-accent border-primary/50"
                      : "bg-sidebar-accent"
                  }`}
                  onClick={() => switchChat(chat.id)}
                >
                  <div className="flex items-center gap-2">
                    <MessageSquare className="w-4 h-4 text-muted-foreground flex-shrink-0" />
                    <span className="text-sm truncate">{chat.title}</span>
                  </div>
                </Card>
              ))
            )}
          </div>
        </ScrollArea>

        {/* User Profile Section */}
        <div className="p-4 border-t border-sidebar-border">
          <Card className="p-3 bg-sidebar-accent border-sidebar-border">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center">
                <User className="w-4 h-4 text-primary" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium truncate">
                  {profile?.full_name || "User"}
                </p>
                <p className="text-xs text-muted-foreground truncate">
                  {profile?.email || user?.email}
                </p>
              </div>
            </div>
            <Separator className="mb-3" />
            <Button
              variant="ghost"
              size="sm"
              className="w-full justify-start text-muted-foreground hover:text-foreground"
              onClick={signOut}
            >
              <LogOut className="w-4 h-4 mr-2" />
              Sign Out
            </Button>
          </Card>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Messages */}
        <ScrollArea className="flex-1 p-6">
          <div className="max-w-3xl mx-auto space-y-6">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
              >
                <Card
                  className={`p-4 max-w-[80%] ${
                    message.role === "user"
                      ? "bg-primary text-primary-foreground"
                      : "bg-card border-border"
                  }`}
                >
                  <div className="text-sm leading-relaxed prose prose-sm max-w-none dark:prose-invert prose-p:my-2 prose-ul:my-2 prose-ol:my-2 prose-li:my-1 prose-headings:my-2 [&_ul]:list-disc [&_ul]:pl-6 [&_ul]:list-outside [&_ol]:list-decimal [&_ol]:pl-6 [&_ol]:list-outside [&_li]:ml-0">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {message.content}
                    </ReactMarkdown>
                  </div>
                </Card>
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start">
                <Card className="p-4 bg-card border-border">
                  <div className="flex gap-2">
                    <div className="w-2 h-2 bg-primary rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: "0.2s" }}></div>
                    <div className="w-2 h-2 bg-primary rounded-full animate-bounce" style={{ animationDelay: "0.4s" }}></div>
                  </div>
                </Card>
              </div>
            )}
          </div>
        </ScrollArea>

        {/* Suggested Prompts */}
        {isEmptyChat && (
          <div className="px-4 py-3">
            <div className="max-w-3xl mx-auto space-y-3">
              <div className="flex items-center gap-2 mb-3">
                <Sparkles className="w-4 h-4 text-primary" />
                <p className="text-muted-foreground text-sm">Try asking about:</p>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {suggestedPrompts.map((prompt, index) => (
                  <Card
                    key={index}
                    className="p-4 bg-card border-border hover:bg-accent/50 cursor-pointer transition-colors"
                    onClick={() => handleSend(prompt)}
                  >
                    <div className="flex items-start gap-3">
                      <MessageSquare className="w-5 h-5 text-primary flex-shrink-0 mt-0.5" />
                      <p className="text-sm">{prompt}</p>
                    </div>
                  </Card>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Input Area */}
        <div className="border-t border-border p-4">
          <div className="max-w-3xl mx-auto">
            <div className="flex gap-2">
              <Input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === "Enter" && handleSend()}
                placeholder="Ask about NASA bioscience research..."
                className="flex-1 bg-input border-border"
                disabled={isLoading}
              />
              <Button
                onClick={() => handleSend()}
                disabled={isLoading || !input.trim()}
                className="bg-accent hover:bg-accent/90"
              >
                <Send className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Chat;
