/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { 
  LayoutDashboard, 
  Lightbulb, 
  Mail, 
  Users, 
  UserSearch, 
  Bot, 
  Bell, 
  Settings, 
  Bolt, 
  TrendingUp, 
  Clock, 
  BadgeCheck, 
  ShieldCheck,
  ChevronRight,
  Send,
  Plus,
  ArrowRight,
  MoreVertical,
  Paperclip,
  CheckCircle2,
  AlertCircle,
  Copy,
  ExternalLink,
  Download,
  Search,
  MapPin,
  TrendingDown,
  BookOpen,
  FileText,
  Map,
  Target
} from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import { Screen, Lead, EmailDraft, Metric } from './types';

// Mock Data
const METRICS: Metric[] = [
  { label: 'Leads this week', value: '9', change: '+12%', status: 'up', icon: 'trending_up' },
  { label: 'Emails pending', value: '2', change: 'Action req.', status: 'warning', icon: 'schedule' },
  { label: 'Open positions', value: '1', change: 'Active hiring', status: 'normal', icon: 'badge' },
  { label: 'CS queries flagged', value: '0', change: 'Clear', status: 'success', icon: 'security' },
];

const LEADS: Lead[] = [
  {
    id: '1',
    name: 'Sarah Chen',
    role: 'CTO @ GreenFlow Systems',
    company: 'GreenFlow Systems',
    avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuB5tVfMZHMTzYYrmjdE2UtjiPrdWG6Bgz56bPWsgXth5PdwOsL-RzkhRIPO-9LZ-xLCTexupsF1DG3Dw74I7nl4-iKZyF-IldzFyB8jdL-_2dUVNTeKqm0vtyhyUvrTUj74KSpuY_Z8asN7BNupCDSVt5_1uu0c2ggM6W5lsggDIjTe_1bBZ5-Vc28rF8HSP3I7h7EhOkbyIXAvtakKnIPtuGHVbAvkqfqY0uSh_ZFtX8E7ifmHMknIxVc27n-JXYCeD-NXucqjAmM',
    fitScore: 9,
    description: 'Previously led engineering at Salesforce. Looking for bespoke AI implementation partners. High alignment with our Sovereign Engine core.',
    tags: ['AI-Match: Enterprise', 'Lead-Source: LinkedIn']
  },
  {
    id: '2',
    name: 'Raj Patel',
    role: 'Founder @ Stealth Robotics',
    company: 'Stealth Robotics',
    avatar: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBJK7FHjSfv_vtJj_qKUNG7qlg52MNOsV-ZMZkaowfwub1g1nuWvZkcvLFldTJ283gyp4H7Fys53UYRi-TGkQJbBoEAm96iDq941fz5SwnQcohrBlQBBUM4EoHRC3YVKCofLx94SqHOj1RqbFGHlDT4Y8k5gIJ0XjMmnqy_k9wIl_rZ6tQqrLHbSztKnJhdU6IVqiZSBwpfutNyp0f6hOza3qnhEhhHS_B5pYuLIyVye8yg-vctt9T8P5pnUuloeTwAoKYURmpUQUw',
    fitScore: 6,
    description: 'Series A founder seeking operational efficiency frameworks. Potential high-growth account but limited budget currently.',
    tags: ['AI-Match: Startup', 'Lead-Source: Referral']
  }
];

const EMAIL_DRAFTS: EmailDraft[] = [
  { id: '1', recipient: 'alex@ventures.com', type: 'Meeting Request', subject: 'Meeting request for Q3 roadmap', preview: "I've been following your work on the Sovereign Engine and would love to..." },
  { id: '2', recipient: 'sarah@techco.com', type: 'Question', subject: 'Question about pricing', preview: "Quick question regarding the data privacy protocols mentioned in..." }
];

export default function App() {
  const [currentScreen, setCurrentScreen] = useState<Screen>('dashboard');

  const renderScreen = () => {
    switch (currentScreen) {
      case 'dashboard': return <Dashboard />;
      case 'intel': return <Intel />;
      case 'emails': return <Emails />;
      case 'talent': return <Talent />;
      case 'leads': return <Leads />;
      case 'cs-bot': return <CSBot />;
      case 'brief': return <Brief />;
      default: return <Dashboard />;
    }
  };

  return (
    <div className="flex min-h-screen bg-surface-0 text-text-primary selection:bg-brand-primary/30 font-sans overflow-hidden relative">
      {/* Background Ambient Glows */}
      <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
        <motion.div 
          animate={{ 
            scale: [1, 1.2, 1],
            x: [0, 100, 0],
            y: [0, 50, 0],
            opacity: [0.05, 0.1, 0.05]
          }}
          transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
          className="absolute -top-1/4 -left-1/4 w-[1000px] h-[1000px] bg-brand-primary rounded-full blur-[150px]"
        />
        <motion.div 
          animate={{ 
            scale: [1.2, 1, 1.2],
            x: [0, -100, 0],
            y: [0, -50, 0],
            opacity: [0.03, 0.08, 0.03]
          }}
          transition={{ duration: 25, repeat: Infinity, ease: "linear" }}
          className="absolute -bottom-1/4 -right-1/4 w-[800px] h-[800px] bg-brand-primary-gradient rounded-full blur-[150px]"
        />
      </div>

      {/* SideNavBar */}
      <aside className="fixed left-0 top-0 h-screen w-[260px] bg-surface-0 border-r border-surface-border flex flex-col z-50">
        <div className="p-10 pt-12">
          <h1 className="text-2xl font-black tracking-tighter text-white flex items-center gap-3">
            <div className="w-10 h-10 bg-brand-primary rounded-xl flex items-center justify-center shadow-[0_0_20px_rgba(124,58,237,0.4)]">
              <Bot className="text-white" size={24} />
            </div>
            FounderOS
          </h1>
        </div>
        
        <nav className="flex-1 px-6 space-y-6">
          <div className="space-y-1">
            <p className="px-4 text-[10px] font-bold text-text-dim uppercase tracking-[0.2em] mb-4">Intelligence</p>
            <NavButton label="Dashboard" icon={<LayoutDashboard size={20} />} active={currentScreen === 'dashboard'} onClick={() => setCurrentScreen('dashboard')} />
            <NavButton label="Intel" icon={<Lightbulb size={20} />} active={currentScreen === 'intel'} onClick={() => setCurrentScreen('intel')} />
          </div>

          <div className="space-y-1">
            <p className="px-4 text-[10px] font-bold text-text-dim uppercase tracking-[0.2em] mb-4">Operations</p>
            <NavButton label="Emails" icon={<Mail size={20} />} active={currentScreen === 'emails'} onClick={() => setCurrentScreen('emails')} />
            <NavButton label="Talent" icon={<Users size={20} />} active={currentScreen === 'talent'} onClick={() => setCurrentScreen('talent')} />
            <NavButton label="Leads" icon={<UserSearch size={20} />} active={currentScreen === 'leads'} onClick={() => setCurrentScreen('leads')} />
            <NavButton label="CS Bot" icon={<Bot size={20} />} active={currentScreen === 'cs-bot'} onClick={() => setCurrentScreen('cs-bot')} />
          </div>

          <div className="space-y-1">
            <p className="px-4 text-[10px] font-bold text-text-dim uppercase tracking-[0.2em] mb-4">System</p>
            <NavButton label="Design Brief" icon={<BookOpen size={20} />} active={currentScreen === 'brief'} onClick={() => setCurrentScreen('brief')} />
          </div>
        </nav>

        <div className="p-6 mt-auto border-t border-surface-border bg-white/[0.01]">
          <div className="flex items-center gap-4 p-2 cursor-pointer hover:bg-white/5 rounded-xl transition-all">
            <div className="w-10 h-10 rounded-full border border-surface-border-light p-0.5">
              <img 
                src="https://lh3.googleusercontent.com/aida-public/AB6AXuAJoAWKwOdxAXwKb_pgUygQOXUwwSew_DHpmVV1hCQZUHHB-6A-IU4SCSALhG3uNpBilwM9U2k4qFciZ6BiGAJOC-NjgdWIBfVs1iVnbRsXz-qZ5ipH28HSx0rugPsVwakTlhKrRjNRpC_N8CyTgzPXCJJjIXRrpWKLkYKSIsogU6z_MQqWYlteRzfS8oCIZL8Is8Q-i7Dq40SiOebYDxkIJbmLmIF8JaigKWe-CnnHWOI-ucM9nl8_QP0Fdvq4BIGUAld94pSIDo4" 
                alt="Profile" 
                className="w-full h-full rounded-full object-cover"
                referrerPolicy="no-referrer"
              />
            </div>
            <div className="min-w-0">
              <p className="text-sm font-bold text-white truncate">Founder User</p>
              <p className="text-[10px] font-medium text-text-dim uppercase tracking-wider">Pro Tier Agent</p>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 ml-[260px] flex flex-col min-w-0 bg-surface-0">
        <header className="sticky top-0 h-20 z-40 bg-surface-0/60 backdrop-blur-xl flex items-center justify-between px-12 border-b border-surface-border">
          <div>
            <h2 className="text-2xl font-black text-white tracking-tight capitalize">{currentScreen.replace('-', ' ')}</h2>
            <p className="text-[10px] text-text-dim font-bold uppercase tracking-widest mt-0.5">Updated 6:32 AM • System Nominal</p>
          </div>
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-success animate-pulse shadow-[0_0_8px_#10B981]" />
              <span className="text-[10px] font-bold text-text-dim uppercase tracking-widest">Global Status: Active</span>
            </div>
            <div className="h-6 w-px bg-surface-border" />
            <div className="flex items-center gap-2">
              <button className="text-text-secondary hover:text-white transition-colors p-2 hover:bg-white/5 rounded-lg"><Bell size={20} /></button>
              <button className="text-text-secondary hover:text-white transition-colors p-2 hover:bg-white/5 rounded-lg"><Settings size={20} /></button>
            </div>
            <button className="btn-skew-reveal scale-90 group">
              <Bolt size={14} className="fill-current relative z-10" />
              <span>Sync All Agents</span>
            </button>
          </div>
        </header>

        <main className="p-12 overflow-y-auto w-full no-scrollbar max-w-7xl mx-auto">
          <AnimatePresence mode="wait">
            <motion.div
              key={currentScreen}
              initial={{ opacity: 0, scale: 0.98, y: 10 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 1.02, y: -10 }}
              transition={{ duration: 0.3, ease: [0.19, 1, 0.22, 1] }}
            >
              {renderScreen()}
            </motion.div>
          </AnimatePresence>
        </main>
      </div>
    </div>
  );
}

function NavButton({ icon, label, active, onClick }: { icon: React.ReactNode, label: string, active?: boolean, onClick: () => void }) {
  return (
    <button 
      onClick={onClick}
      className={`sidebar-item ${active ? 'sidebar-item-active' : ''}`}
    >
      <span className={`shrink-0 transition-colors ${active ? 'sidebar-icon-active' : 'group-hover:text-text-primary'}`}>{icon}</span>
      <span className="text-sm font-semibold tracking-tight">{label}</span>
      {active && (
        <motion.div 
          layoutId="active-pill"
          className="absolute left-0 top-3 bottom-3 w-1 bg-brand-primary rounded-r-full shadow-[0_0_10px_#7C3AED]"
        />
      )}
    </button>
  );
}

// --- Screens ---

// Animation Variants
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
      delayChildren: 0.2
    }
  }
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { 
    opacity: 1, 
    y: 0,
    transition: { duration: 0.5, ease: [0.19, 1, 0.22, 1] }
  }
};

function Dashboard() {
  const [isBriefingOpen, setIsBriefingOpen] = useState(false);

  return (
    <motion.div 
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="space-y-12 pb-24 relative z-10"
    >
      {/* Overnight Summary Hero */}
      <motion.section variants={itemVariants} className="card-premium p-10 relative overflow-hidden group">
        <div className="absolute top-0 right-0 w-96 h-96 bg-brand-primary/5 blur-[120px] rounded-full -mr-48 -mt-48 animate-pulse" />
        <div className="relative z-10 grid grid-cols-1 lg:grid-cols-3 gap-12 items-center">
          <div className="lg:col-span-2 space-y-6">
            <div className="flex items-center gap-4">
              <span className="badge-ai">Agent Intelligence</span>
              <span className="text-[10px] font-bold text-text-dim uppercase tracking-widest">• Updated 4 mins ago</span>
            </div>
            <h1 className="text-4xl font-black text-white leading-tight">
              FounderOS identified <span className="text-brand-primary">12 high-priority</span> operational opportunities overnight.
            </h1>
            <p className="text-lg text-text-secondary leading-relaxed max-w-2xl">
              Market signals suggest a favorable expansion window in the vertical AI sector. Your talent pipeline has shifted towards technical leadership, with 3 Tier-1 candidates awaiting outreach.
            </p>
            <div className="flex gap-4 pt-4">
              <button className="btn-skew-reveal px-8 py-3 text-base group">
                <span>Initialize Workstream</span>
              </button>
              <button className="btn-secondary px-8 py-3 text-base group">
                <span>View Full Briefing</span>
              </button>
            </div>
          </div>
          <div className="hidden lg:block space-y-6 bg-white/[0.02] border border-surface-border p-8 rounded-2xl backdrop-blur-sm">
            <div className="space-y-4">
              <p className="text-[10px] font-bold text-text-dim uppercase tracking-[0.2em]">Confidence Indicator</p>
              <div className="flex items-end gap-1 h-12">
                {[4, 7, 5, 9, 8, 10, 10].map((h, i) => (
                  <motion.div 
                    key={i}
                    initial={{ height: 0 }}
                    animate={{ height: `${h * 10}%` }}
                    transition={{ delay: 0.5 + i * 0.1, duration: 1, ease: 'easeOut' }}
                    className="flex-1 bg-brand-primary rounded-t-sm"
                  />
                ))}
              </div>
              <motion.div 
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 1.2 }}
                className="flex justify-between items-center bg-surface-base p-3 rounded-xl border border-surface-border"
              >
                <span className="text-sm font-bold text-white">98.2% Accuracy</span>
                <BadgeCheck size={16} className="text-brand-primary" />
              </motion.div>
            </div>
          </div>
        </div>
      </motion.section>

      {/* Striking Metrics */}
      <motion.section variants={containerVariants} className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard variants={itemVariants} 
          label="Leads this week" 
          value="12" 
          change="+14%" 
          color="text-success" 
          icon={<UserSearch size={20} />} 
          trend="up"
        />
        <MetricCard variants={itemVariants} 
          label="Emails pending" 
          value="04" 
          change="2 urgent" 
          color="text-warning" 
          icon={<Mail size={20} />} 
          trend="warning"
        />
        <MetricCard variants={itemVariants} 
          label="Talent Matches" 
          value="18" 
          change="3 premium" 
          color="text-brand-primary" 
          icon={<Users size={20} />} 
          trend="up"
        />
        <MetricCard variants={itemVariants} 
          label="Bot Activity" 
          value="961" 
          change="-4 incidents" 
          color="text-success" 
          icon={<Bot size={20} />} 
          trend="up"
        />
      </motion.section>

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-12">
        <motion.section variants={containerVariants} className="lg:col-span-3 space-y-8">
          <motion.div variants={itemVariants} className="flex justify-between items-center px-2">
            <div>
              <h3 className="text-xl font-black text-white tracking-tight">System Intel: Recent Leads</h3>
              <p className="text-xs text-text-dim font-bold uppercase tracking-widest mt-1">Sovereign Agent Analyzed</p>
            </div>
            <motion.button whileHover={{ x: 5 }} className="text-xs text-brand-primary font-bold hover:underline tracking-widest uppercase">Explore Database</motion.button>
          </motion.div>
          <div className="space-y-4">
            <LeadRow variants={itemVariants} name="Sarah Chen" score={9} summary="Previously led engineering at Salesforce. High alignment with core engine." label="Premium Match" />
            <LeadRow variants={itemVariants} name="Raj Patel" score={6} summary="Founder at stealth startup. Seeking operational efficiency frameworks." />
            <LeadRow variants={itemVariants} name="Elena Rodriguez" score={8} summary="VP Product at growth-stage fintech. Interested in automation suite." label="Qualified" />
          </div>
        </motion.section>

        <motion.section variants={containerVariants} className="lg:col-span-2 space-y-8">
          <motion.div variants={itemVariants} className="flex justify-between items-center px-2">
            <div>
              <h3 className="text-xl font-black text-white tracking-tight">Draft Queue</h3>
              <p className="text-xs text-text-dim font-bold uppercase tracking-widest mt-1">Ready for Approval</p>
            </div>
            <motion.button whileHover={{ x: 5 }} className="text-xs text-brand-primary font-bold hover:underline tracking-widest uppercase">Open Inbox</motion.button>
          </motion.div>
          <div className="space-y-4">
            <EmailRow variants={itemVariants} sender="alex@ventures.io" subject="Meeting request for Q3 roadmap" time="12m ago" />
            <EmailRow variants={itemVariants} sender="sarah@techco.global" subject="Question about pricing tiers" time="1h ago" />
            <EmailRow variants={itemVariants} sender="investor@funds.vc" subject="Product-led growth follow-up" time="2h ago" />
          </div>
        </motion.section>
      </div>

      <motion.section variants={itemVariants} className="card-premium overflow-hidden">
        <div 
          className="p-8 cursor-pointer hover:bg-white/[0.02] transition-colors"
          onClick={() => setIsBriefingOpen(!isBriefingOpen)}
        >
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-6">
              <div className="w-14 h-14 rounded-2xl bg-brand-primary/10 border border-brand-primary/20 flex items-center justify-center text-brand-primary shadow-inner">
                <TrendingUp size={28} />
              </div>
              <div>
                <h3 className="text-xl font-black text-white tracking-tight">Macro Market Briefing</h3>
                <p className="text-sm font-medium text-text-secondary">AI synthesis of global SaaS trends and competitor shifts</p>
              </div>
            </div>
            <motion.div
              animate={{ rotate: isBriefingOpen ? 180 : 0 }}
              transition={{ duration: 0.3, ease: 'backOut' }}
            >
              <div className="w-10 h-10 rounded-full bg-white/5 border border-surface-border flex items-center justify-center text-text-dim">
                <ChevronRight size={24} className="rotate-90" />
              </div>
            </motion.div>
          </div>
        </div>
        
        <AnimatePresence>
          {isBriefingOpen && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              className="overflow-hidden border-t border-surface-border bg-white/[0.01]"
            >
              <div className="p-10 space-y-6 text-base text-text-secondary leading-relaxed">
                <p>FounderOS agent detects a significant shift towards <span className="text-white font-bold">Vertical AI solutions</span> in the mid-market segment. Legacy SaaS incumbents (Salesforce, HubSpot) are struggling to pivot their core architecture, creating a high-conviction 12-18 month window for rapid ecosystem capture.</p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8 pt-6">
                  <div className="space-y-4">
                    <div className="badge-premium">Competitive Edge</div>
                    <p className="text-sm border-l-2 border-brand-primary pl-4 py-1 italic">"Proprietary Sovereign Drafting is currently outperforming OpenAI's internal benchmarks by 22% in context-aware creative accuracy."</p>
                  </div>
                  <div className="space-y-4">
                    <div className="badge-premium">Sentiment Analysis</div>
                    <p className="text-sm border-l-2 border-brand-primary pl-4 py-1 italic">"Enterprise buyers are increasingly favoring Agency-First workflows over simple LLM wrappers. Your CS Bot integration demand is up 40% QoQ."</p>
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.section>
    </motion.div>
  );
}

function MetricCard({ label, value, change, color, icon, trend, ...props }: any) {
  return (
    <motion.div {...props} className="card-premium p-8 group cursor-default relative overflow-hidden">
      <div className="flex justify-between items-start relative z-10">
        <div className="space-y-4 text-left">
          <p className="text-[10px] font-bold text-text-dim uppercase tracking-[0.2em]">{label}</p>
          <div className="space-y-1">
            <h4 className={`text-4xl font-black text-white ${color}`}>{value}</h4>
            <div className="flex items-center gap-2">
              {trend === 'up' && <TrendingUp size={12} className="text-success" />}
              {trend === 'warning' && <AlertCircle size={12} className="text-warning" />}
              <span className={`text-[10px] font-bold ${trend === 'up' ? 'text-success' : trend === 'warning' ? 'text-warning' : 'text-text-dim'}`}>{change}</span>
            </div>
          </div>
        </div>
        <div className="w-12 h-12 rounded-xl bg-white/[0.03] border border-surface-border flex items-center justify-center text-text-muted group-hover:text-white transition-colors">
          {icon}
        </div>
      </div>
      <div className="absolute -bottom-4 -right-4 w-24 h-24 bg-brand-primary/5 blur-2xl rounded-full opacity-0 group-hover:opacity-100 transition-opacity" />
    </motion.div>
  );
}

function LeadRow({ name, score, summary, label, ...props }: any) {
  return (
    <motion.div {...props} className="group flex items-start gap-6 p-6 rounded-2xl card-premium hover:translate-x-1 transition-all">
      <div className="relative shrink-0">
        <div className="w-14 h-14 rounded-2xl bg-surface-2 border border-surface-border flex items-center justify-center text-xl font-black text-white shadow-lg overflow-hidden">
          {name[0]}
        </div>
        <div className={`absolute -bottom-1 -right-1 w-5 h-5 rounded-full border-2 border-surface-1 flex items-center justify-center text-[10px] font-black text-white shadow-lg ${score >= 8 ? 'bg-success' : score >= 6 ? 'bg-warning' : 'bg-brand-primary'}`}>
          {score}
        </div>
      </div>
      <div className="flex-1 min-w-0 space-y-2">
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-3">
            <h4 className="font-bold text-white text-base">{name}</h4>
            {label && <span className="badge-ai text-[8px] px-1.5 py-0">{label}</span>}
          </div>
          <span className="text-[10px] font-black text-text-dim uppercase tracking-widest">Confidence: 94%</span>
        </div>
        <p className="text-sm text-text-secondary leading-relaxed line-clamp-2 italic opacity-80 border-l border-surface-border pl-4">"{summary}"</p>
        <div className="flex items-center gap-4 pt-2">
          <button className="text-[10px] font-bold text-brand-primary uppercase tracking-widest hover:underline">Connect via Signal</button>
          <div className="w-1 h-1 rounded-full bg-text-muted" />
          <button className="text-[10px] font-bold text-text-muted uppercase tracking-widest hover:text-white">Ignore</button>
        </div>
      </div>
    </motion.div>
  );
}

function EmailRow({ sender, subject, time, ...props }: any) {
  return (
    <motion.div {...props} className="group flex items-center justify-between p-6 rounded-2xl card-premium hover:bg-white/[0.02] transition-all">
      <div className="min-w-0 space-y-1">
        <div className="flex items-center gap-3">
          <h4 className="font-bold text-white text-sm truncate">{sender}</h4>
          <span className="text-[10px] font-medium text-text-dim">{time}</span>
        </div>
        <p className="text-xs text-text-secondary truncate font-medium opacity-70">{subject}</p>
      </div>
      <button className="btn-primary px-4 py-2 text-[10px] uppercase tracking-widest font-black">Approve</button>
    </motion.div>
  );
}

function Intel() {
  const [loading, setLoading] = useState(false);

  const handleAnalyze = () => {
    setLoading(true);
    setTimeout(() => setLoading(false), 2000);
  };

  return (
    <motion.div 
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="max-w-5xl mx-auto space-y-12 pb-24 relative z-10"
    >
      <motion.section variants={itemVariants} className="card-premium p-4 flex flex-col md:flex-row items-center gap-4">
        <div className="flex-1 w-full flex items-center gap-4 px-6 py-4 bg-white/[0.02] rounded-xl border border-surface-border">
          <Search size={22} className="text-brand-primary" />
          <input className="bg-transparent border-none text-xl text-white placeholder:text-text-muted focus:ring-0 w-full font-black tracking-tight" placeholder="Identify Company" defaultValue="Notion" />
        </div>
        <div className="flex-1 w-full flex items-center gap-4 px-6 py-4 bg-white/[0.02] rounded-xl border border-surface-border">
          <TrendingUp size={22} className="text-brand-primary" />
          <input className="bg-transparent border-none text-xl text-white placeholder:text-text-muted focus:ring-0 w-full font-black tracking-tight" placeholder="Declare Market" defaultValue="SaaS / Productivity" />
        </div>
        <button 
          onClick={handleAnalyze}
          className="btn-skew-reveal py-5 px-10 text-lg group"
        >
          <div className="flex items-center gap-3 relative z-10">
            {loading ? <Clock size={20} className="animate-spin" /> : <TrendingUp size={20} />}
            <span>{loading ? 'Agents Sourcing...' : 'Execute Analysis'}</span>
          </div>
        </button>
      </motion.section>

      {loading ? (
        <div className="flex flex-col items-center justify-center py-32 space-y-8">
          <div className="relative">
            <div className="absolute inset-0 bg-brand-primary blur-3xl opacity-20 animate-pulse" />
            <motion.div
              initial={{ rotate: 0 }}
              animate={{ rotate: 360 }}
              transition={{ duration: 4, repeat: Infinity, ease: "linear" }}
            >
              <Bot size={84} className="text-brand-primary relative z-10" />
            </motion.div>
          </div>
          <p className="text-2xl font-black text-white tracking-tight animate-pulse">Sourcing Sovereign Intelligence...</p>
        </div>
      ) : (
        <motion.div 
          variants={containerVariants}
          className="space-y-12"
        >
          <motion.section variants={itemVariants} className="space-y-8">
            <div className="text-center space-y-2">
              <h2 className="text-3xl font-black text-white tracking-tighter">SWOT Matrix</h2>
              <p className="text-text-dim font-bold uppercase tracking-widest text-xs">AI-Derived Strategic Invariants</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <SwotCard variants={itemVariants} title="Strengths" status="up" items={["Dominant market share", "Premium brand perception", "Network effects"]} />
              <SwotCard variants={itemVariants} title="Weaknesses" status="down" items={["High customer acquisition cost", "Legacy tech debt", "Limited mobile optimization"]} />
              <SwotCard variants={itemVariants} title="Opportunities" color="text-brand-primary" status="normal" border="border-brand-primary/40" items={["AI-native feature expansion", "Underserved EU markets", "Enterprise tier growth"]} />
              <SwotCard variants={itemVariants} title="Threats" color="text-warning" status="error" border="border-warning/40" items={["Emerging open-source clones", "Regulatory scrutiny", "Talent poaching"]} />
            </div>
          </motion.section>

          <motion.div variants={itemVariants} className="grid grid-cols-1 md:grid-cols-5 gap-12 pt-12 border-t border-surface-border">
            <div className="md:col-span-3 space-y-8">
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <div className="w-1 h-6 bg-brand-primary rounded-full shadow-[0_0_10px_#7C3AED]" />
                  <h3 className="text-xl font-black text-white tracking-tight">Market Synopsis</h3>
                </div>
                <p className="text-lg text-text-secondary leading-relaxed font-medium">The productivity sector is experiencing a <span className="text-white">massive consolidation wave</span>. Founders are aggressively pivoting from isolated point solutions toward high-integrity AI hubs like FounderOS.</p>
              </div>
              
              <div className="space-y-4">
                <h3 className="text-[10px] font-bold text-text-dim uppercase tracking-[0.2em]">Competitor Cluster</h3>
                <div className="flex flex-wrap gap-3">
                  {["Linear", "Notion", "ClickUp", "Monday", "Superhuman"].map(c => (
                    <span key={c} className="badge-premium border-surface-border-light hover:border-brand-primary/50 cursor-default transition-colors">{c}</span>
                  ))}
                </div>
              </div>
            </div>
            <div className="md:col-span-2 space-y-4 bg-white/[0.02] border border-surface-border p-8 rounded-3xl backdrop-blur-md">
              <h3 className="text-sm font-black text-white uppercase tracking-widest">Executive Forecast</h3>
              <p className="text-base text-text-dim italic leading-relaxed font-medium border-l-2 border-brand-primary/30 pl-6 py-2">
                "The next 12 months will be defined by <span className="text-text-secondary">autonomous agency</span>. Winning organizations will no longer use tools; they will oversee agents that perform end-to-end business functions with 99.9% reliability."
              </p>
            </div>
          </motion.div>
        </motion.div>
      )}
    </motion.div>
  );
}

function SwotCard({ title, items, status, color, border, ...props }: any) {
  const defaultBorder = status === 'up' ? 'border-success/40' : status === 'down' ? 'border-error/40' : status === 'error' ? 'border-warning/40' : 'border-brand-primary/40';
  const textColor = color || (status === 'up' ? 'text-success' : status === 'down' ? 'text-error' : status === 'error' ? 'text-warning' : 'text-brand-primary');

  return (
    <motion.div {...props} className={`card-premium p-8 border-t-4 ${border || defaultBorder} hover:shadow-[0_0_30px_rgba(255,255,255,0.02)]`}>
      <div className="flex justify-between items-center mb-6">
        <h3 className={`${textColor} font-black uppercase tracking-[0.2em] text-xs`}>{title}</h3>
        {status === 'up' && <TrendingUp size={16} className="text-success" />}
        {status === 'down' && <TrendingDown size={16} className="text-error" />}
      </div>
      <ul className="space-y-4">
        {items.map(item => (
          <li key={item} className="flex items-start gap-4 text-text-secondary text-base font-medium">
            <CheckCircle2 size={16} className={`mt-1 shrink-0 ${textColor} opacity-40`} />
            <span>{item}</span>
          </li>
        ))}
      </ul>
    </motion.div>
  );
}


function InsightCard({ title, desc, icon, content }: { title: string, desc?: string, icon: React.ReactNode, content?: React.ReactNode }) {
  return (
    <div className="glass-card p-8 rounded-xl border border-white/10 relative overflow-hidden group hover:translate-y-[-4px] transition-all">
      <div className="absolute top-0 right-0 w-32 h-32 bg-brand-primary/10 rounded-full -mr-16 -mt-16 blur-2xl group-hover:bg-brand-primary/20 transition-all"></div>
      <span className="text-brand-primary mb-5 block relative z-10">{icon}</span>
      <h4 className="text-xl font-bold text-white mb-3 relative z-10">{title}</h4>
      {desc && <p className="text-sm text-text-dim font-medium leading-relaxed relative z-10">{desc}</p>}
      <div className="relative z-10">{content}</div>
    </div>
  );
}


function Emails() {
  return (
    <motion.div 
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="max-w-4xl mx-auto space-y-12 pb-32 relative z-10"
    >
      <motion.div variants={itemVariants} className="flex justify-between items-end px-2">
        <div>
          <h2 className="text-3xl font-black text-white tracking-tighter">Sovereign Inbox</h2>
          <p className="text-text-dim font-bold uppercase tracking-widest text-[10px] mt-1">Autonomous Drafting Active</p>
        </div>
        <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }} className="btn-secondary">
          <Plus size={16} /> New Workstream
        </motion.button>
      </motion.div>

      <motion.div variants={containerVariants} className="space-y-6">
        <EmailCard 
          variants={itemVariants}
          sender="Alex Rivera" 
          subject="Meeting request for Q3 roadmap" 
          date="Oct 12 • 4m ago"
          badge="High Signal"
          draft="Hi Alex, I've reviewed the Q3 objectives. Let's get a call on the books for next week to dive deeper into those traction metrics."
        />
        <EmailCard 
          variants={itemVariants}
          sender="Sarah TechCo" 
          subject="Question about pricing" 
          date="Oct 12 • 1h ago"
          badge="Enterprise"
          draft="Hi Sarah, our pricing tiers scale with your volume. For your team size, the Pro plan would be most effective. I've attached the matrix."
        />
        <EmailCard 
          variants={itemVariants}
          sender="SeedFund VC" 
          subject="Follow-up on growth metrics" 
          date="Oct 11 • 2h ago"
          badge="Investor"
          draft="Happy to share those numbers. We've seen a 40% MoM increase in active agents. Let me know if you need the full cohort analysis."
        />
      </motion.div>
    </motion.div>
  );
}

function EmailCard({ sender, subject, date, badge, draft, ...props }: any) {
  return (
    <motion.div {...props} className="card-premium p-8 hover:bg-white/[0.02] relative group">
      <div className="flex justify-between items-start mb-6">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-brand-primary/10 border border-brand-primary/20 flex items-center justify-center text-brand-primary font-black text-lg">
            {sender[0]}
          </div>
          <div>
            <h4 className="font-bold text-white text-base tracking-tight">{sender}</h4>
            <p className="text-xs text-text-dim font-medium">{subject}</p>
          </div>
        </div>
        <div className="text-right space-y-1">
          <span className="text-[10px] font-bold text-text-muted uppercase tracking-widest">{date}</span>
          {badge && (
            <div className="block">
              <span className="badge-ai text-[8px] px-1.5 py-0.5">{badge}</span>
            </div>
          )}
        </div>
      </div>

      <div className="bg-surface-0/50 border border-surface-border p-6 rounded-2xl mb-8 relative">
        <div className="absolute top-4 right-4 text-brand-primary opacity-20">
          <Bot size={24} />
        </div>
        <div className="flex items-center gap-2 mb-3">
          <div className="w-1.5 h-1.5 rounded-full bg-brand-primary animate-pulse" />
          <span className="text-[10px] font-black text-brand-primary uppercase tracking-[0.2em]">Sovereign Draft</span>
        </div>
        <p className="text-sm text-text-secondary italic leading-relaxed font-medium">"{draft}"</p>
      </div>

      <div className="flex gap-4">
        <button className="btn-skew-reveal flex-1 py-3 text-xs uppercase tracking-[0.2em] font-black group">
          <span>Approve & Send</span>
        </button>
        <button className="btn-secondary flex-1 py-3 text-xs uppercase tracking-[0.2em] font-black group">
          <span>Refine Draft</span>
        </button>
      </div>
    </motion.div>
  );
}


function Talent() {
  return (
    <motion.div 
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="max-w-6xl mx-auto space-y-12 pb-32"
    >
      <motion.div variants={itemVariants} className="flex justify-between items-end px-2">
        <div>
          <h2 className="text-3xl font-black text-white tracking-tighter">Human Capital Intel</h2>
          <p className="text-text-dim font-bold uppercase tracking-widest text-[10px] mt-1">Autonomous Sourcing Active • 18 matches</p>
        </div>
      </motion.div>

      <motion.section variants={itemVariants} className="card-premium p-8 grid grid-cols-1 md:grid-cols-4 gap-6 items-end bg-white/[0.01]">
        <div className="space-y-3">
          <label className="text-[10px] uppercase font-black text-text-dim tracking-widest">Target Role</label>
          <div className="relative">
            <Users size={14} className="absolute left-4 top-1/2 -translate-y-1/2 text-brand-primary" />
            <input className="w-full bg-surface-base border border-surface-border rounded-xl pl-10 pr-4 py-3 text-sm text-white focus:border-brand-primary focus:ring-1 focus:ring-brand-primary/20 transition-all font-medium" placeholder="Senior Engineer" defaultValue="Senior Engineer" />
          </div>
        </div>
        <div className="space-y-3">
          <label className="text-[10px] uppercase font-black text-text-dim tracking-widest">Geographic Hub</label>
          <div className="relative">
            <MapPin size={14} className="absolute left-4 top-1/2 -translate-y-1/2 text-brand-primary" />
            <input className="w-full bg-surface-base border border-surface-border rounded-xl pl-10 pr-4 py-3 text-sm text-white focus:border-brand-primary focus:ring-1 focus:ring-brand-primary/20 transition-all font-medium" placeholder="San Francisco" defaultValue="San Francisco / Remote" />
          </div>
        </div>
        <div className="space-y-3">
          <label className="text-[10px] uppercase font-black text-text-dim tracking-widest">Experience Level</label>
          <input className="w-full bg-surface-base border border-surface-border rounded-xl px-4 py-3 text-sm text-white focus:border-brand-primary focus:ring-1 focus:ring-brand-primary/20 transition-all font-medium" placeholder="Min. 5 years" defaultValue="5+ Years" />
        </div>
        <button className="btn-skew-reveal h-12 px-8 group">
          <Search size={18} className="relative z-10" /> 
          <span className="uppercase tracking-widest text-xs font-black">Refresh Results</span>
        </button>
      </motion.section>

      <motion.div variants={containerVariants} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <CandidateCard 
          variants={itemVariants}
          name="Sarah Chen" 
          role="Senior Frontend Engineer" 
          loc="San Francisco, CA" 
          score={9.4} 
          previous="cto @ greenflow"
          tags={['React', 'Web3', 'Growth']}
        />
        <CandidateCard 
          variants={itemVariants}
          name="Raj Patel" 
          role="Backend Systems Architect" 
          loc="New York, NY" 
          score={7.8} 
          previous="staff engineer @ stripe"
          tags={['Go', 'Rust', 'Infrastructure']}
        />
        <CandidateCard 
          variants={itemVariants}
          name="Elena Rodriguez" 
          role="Product Growth Lead" 
          loc="Austin, TX / Remote" 
          score={8.9} 
          previous="lead product @ notion"
          tags={['PLG', 'Strategy', 'AI']}
        />
      </motion.div>
    </motion.div>
  );
}

function CandidateCard({ name, role, loc, score, previous, tags, ...props }: any) {
  return (
    <motion.div {...props} className="card-premium p-8 hover:scale-[1.02] relative group">
      <div className="flex justify-between items-start mb-8">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-brand-primary/20 to-brand-primary/5 border border-brand-primary/20 flex items-center justify-center text-2xl font-black text-white shadow-inner">
            {name[0]}
          </div>
          <div>
            <h4 className="font-black text-white text-lg tracking-tight">{name}</h4>
            <p className="text-xs text-text-secondary font-bold uppercase tracking-widest opacity-70">{role}</p>
          </div>
        </div>
        <div className="relative w-12 h-12 flex items-center justify-center">
          <svg className="w-full h-full transform -rotate-90">
            <circle cx="24" cy="24" r="21" fill="transparent" stroke="currentColor" strokeWidth="4" className="text-surface-border" />
            <motion.circle 
              cx="24" cy="24" r="21" 
              fill="transparent" 
              stroke="currentColor" 
              strokeWidth="4" 
              strokeDasharray="132" 
              initial={{ strokeDashoffset: 132 }}
              animate={{ strokeDashoffset: 132 * (1 - score/10) }}
              transition={{ duration: 1.5, ease: 'easeOut' }}
              className="text-brand-primary" 
              strokeLinecap="round" 
            />
          </svg>
          <span className="absolute text-xs font-black text-white">{score}</span>
        </div>
      </div>
      
      <div className="space-y-4 mb-8">
        <div className="flex items-center gap-3">
          <MapPin size={14} className="text-brand-primary opacity-60" />
          <span className="text-sm font-medium text-text-secondary">{loc}</span>
        </div>
        <div className="p-4 rounded-xl bg-white/[0.02] border border-surface-border">
          <p className="text-[10px] font-black text-text-dim uppercase tracking-widest mb-1.5">Sovereign Insight</p>
          <p className="text-xs text-text-secondary leading-relaxed font-medium">Ex-{previous}. Strong alignment with our roadmap for decentralized infrastructure.</p>
        </div>
      </div>

      <div className="flex flex-wrap gap-2 mb-8">
        {tags && tags.map((t: string) => (
          <span key={t} className="text-[9px] font-black uppercase tracking-widest px-2 py-0.5 rounded-md bg-white/5 border border-surface-border text-text-muted">{t}</span>
        ))}
      </div>

      <div className="flex gap-3">
        <button className="btn-skew-reveal flex-1 text-[10px] uppercase font-black py-2.5 group">
          <span>Send Outreach</span>
        </button>
        <button className="btn-secondary px-3 py-2.5 group">
          <Paperclip size={16} />
        </button>
      </div>
    </motion.div>
  );
}

function Leads() {
  return (
    <motion.div 
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="max-w-6xl mx-auto space-y-12 pb-32"
    >
      <motion.header variants={itemVariants} className="flex justify-between items-end border-b border-surface-border pb-12">
        <div>
          <h2 className="text-4xl font-black text-white tracking-tighter mb-2">Qualified Signals</h2>
          <p className="text-base text-text-secondary font-medium">Global engine routing via <span className="text-brand-primary font-bold transition-all hover:shadow-[0_0_10px_#7C3AED]">+1 555-0199</span></p>
        </div>
        <div className="flex gap-4">
           <button className="btn-secondary group">
             <Settings size={18} />
             <span className="text-xs font-black uppercase tracking-widest">Filter Strategy</span>
           </button>
           <button className="btn-skew-reveal group px-6">
             <Download size={18} className="relative z-10" />
             <span className="text-xs font-black uppercase tracking-widest">Export High-Signal</span>
           </button>
        </div>
      </motion.header>

      <motion.div variants={containerVariants} className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <LeadCard 
          variants={itemVariants}
          name="Sarah Chen" 
          duration="4m 20s" 
          score={9.2} 
          summarizes="High volume overhead detected in current stack. Immediate infrastructure transition predicted." 
          status="Qualified"
        />
        <LeadCard 
          variants={itemVariants}
          name="Raj Patel" 
          duration="3m 15s" 
          score={6.4} 
          summarizes="Interest confirmed via side-channel. Restricted by legacy regional oversight committees." 
          status="Monitoring"
        />
      </motion.div>
    </motion.div>
  );
}

function LeadCard({ name, duration, score, summarizes, status, ...props }: any) {
  return (
    <motion.div {...props} className="card-premium p-10 relative group overflow-hidden">
      <div className="absolute top-0 right-0 w-32 h-32 bg-brand-primary/5 blur-3xl opacity-0 group-hover:opacity-100 transition-opacity" />
      <div className="flex justify-between items-start mb-10 relative z-10">
        <div className="flex items-center gap-6">
          <div className="w-16 h-16 rounded-2xl bg-surface-2 border border-surface-border flex items-center justify-center text-2xl font-black text-white shadow-xl group-hover:border-brand-primary/40 transition-colors">
            {name[0]}
          </div>
          <div className="space-y-1">
            <h4 className="font-black text-white text-2xl tracking-tighter">{name}</h4>
            <div className="flex items-center gap-3 text-text-dim text-xs font-bold uppercase tracking-widest">
              <span className="flex items-center gap-1.5"><Clock size={12} /> {duration}</span>
              <span className="w-1 h-1 rounded-full bg-text-muted" />
              <span className="text-brand-primary">{status}</span>
            </div>
          </div>
        </div>
        <div className="text-right">
          <p className="text-[10px] font-black text-text-dim uppercase tracking-[0.2em] mb-1">Qual-Score</p>
          <div className="text-3xl font-black text-white drop-shadow-[0_0_10px_rgba(255,255,255,0.1)]">{score}<span className="text-sm opacity-40">/10</span></div>
        </div>
      </div>

      <div className="grid grid-cols-4 gap-3 mb-10">
        {[
          { l: 'B', v: 'Verified', c: 'text-success' },
          { l: 'A', v: 'Enterprise', c: 'text-success' },
          { l: 'N', v: 'Immediate', c: 'text-success' },
          { l: 'T', v: 'Reviewing', c: 'text-warning' }
        ].map(item => (
          <div key={item.l} className="bg-white/[0.02] border border-surface-border p-4 rounded-2xl text-center space-y-1 hover:border-brand-primary/30 transition-colors">
            <span className={`text-sm font-black ${item.c}`}>{item.l}</span>
            <p className="text-[8px] font-bold text-text-dim uppercase tracking-widest">{item.v}</p>
          </div>
        ))}
      </div>

      <div className="space-y-6 mb-10">
        <div className="space-y-2">
          <p className="text-[10px] font-black text-brand-primary uppercase tracking-[0.2em]">Recommended Protocol</p>
          <div className="p-4 rounded-xl bg-brand-primary/5 border border-brand-primary/10">
            <p className="text-sm text-white font-bold">Initiate Sovereign Demo via Slack bridge + Tier 1 Outreach</p>
          </div>
        </div>
        <p className="text-sm text-text-secondary leading-relaxed italic font-medium opacity-80 border-l-2 border-surface-border pl-6">"{summarizes}"</p>
      </div>

      <div className="flex gap-4">
        <button className="btn-primary flex-1 py-4 text-xs font-black uppercase tracking-widest">Mark Contacted</button>
        <button className="btn-secondary flex-1 py-4 text-xs font-black uppercase tracking-widest">Dismiss Signal</button>
      </div>
    </motion.div>
  );
}

function CSBot() {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
      className="h-[calc(100vh-180px)] flex flex-col md:flex-row overflow-hidden border border-surface-border rounded-3xl card-premium bg-surface-0 shadow-2xl"
    >
      <section className="flex-1 flex flex-col">
        <div className="px-8 py-5 border-b border-surface-border flex items-center justify-between bg-white/[0.01]">
          <div className="flex items-center gap-4">
            <div className="relative">
              <div className="w-2.5 h-2.5 rounded-full bg-success animate-pulse shadow-[0_0_8px_#10B981]" />
            </div>
            <div className="space-y-0.5">
              <h3 className="text-sm font-black text-white uppercase tracking-widest">Agent CS-091 Active</h3>
              <p className="text-[10px] font-bold text-text-dim uppercase tracking-widest">Sovereign Layer Protection</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
             <button className="text-text-dim hover:text-white transition-colors"><MoreVertical size={20} /></button>
          </div>
        </div>

        <motion.div 
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          className="flex-1 overflow-y-auto p-10 space-y-8 no-scrollbar bg-gradient-to-b from-transparent to-brand-primary/[0.02]"
        >
          <ChatMessage variants={itemVariants} type="bot" msg="FounderOS CS Agent ready. I am currently monitoring 42 active sessions with a 99.4% resolution accuracy. How can I optimize your customer operations today?" />
          <ChatMessage variants={itemVariants} type="user" msg="I need to update the global refund policy for our Enterprise tier. Can we automate the initial triage?" />
          <ChatMessage variants={itemVariants} type="bot" flagged msg="Refund policies for Enterprise require manual oversight per your Sovereign Directive 04. I've flagged the triage logic for your immediate review." />
          <ChatMessage variants={itemVariants} type="user" msg="What's the current training progress for the upcoming Logistics specialized agent?" />
          <ChatMessage variants={itemVariants} type="bot" msg="Training is 92.4% complete. 8 outlier signals remain in the queue for manual correction. Expected deployment in 4 hours." />
        </motion.div>

        <div className="p-8 border-t border-surface-border bg-white/[0.01]">
          <div className="flex items-center gap-4 bg-surface-1 border border-surface-border-light rounded-2xl p-3 shadow-2xl focus-within:border-brand-primary/50 transition-all">
            <button className="p-3 text-text-dim hover:text-brand-primary transition-colors hover:bg-white/5 rounded-xl"><Paperclip size={20} /></button>
            <input className="flex-1 bg-transparent border-none focus:ring-0 text-base py-2 text-white placeholder:text-text-muted font-medium" placeholder="Instruct Sovereign Agent..." />
            <motion.button 
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="w-12 h-12 bg-brand-primary text-white rounded-xl flex items-center justify-center hover:bg-brand-primary-gradient transition-all shadow-lg hover:shadow-brand-primary/30 active:scale-95"
            >
              <Send size={20} />
            </motion.button>
          </div>
        </div>
      </section>

      <aside className="w-full md:w-96 border-l border-surface-border bg-white/[0.01] p-8 flex flex-col gap-10 overflow-y-auto no-scrollbar">
        <motion.div variants={containerVariants} initial="hidden" animate="visible" className="space-y-6">
          <div className="flex justify-between items-center">
            <h3 className="text-sm font-black text-white uppercase tracking-widest">Corrective Queue</h3>
            <span className="badge-ai text-[8px] px-1.5 py-0.5">8 Needs Input</span>
          </div>
          <div className="space-y-4">
            <QueueItem variants={itemVariants} label="Enterprise Refund" status="Flagged" color="border-warning/40" score={94} />
            <QueueItem variants={itemVariants} label="Logistics API Edge Case" status="Pending" score={88} />
            <QueueItem variants={itemVariants} label="Bulk Discount Logic" status="Pending" score={91} />
            <QueueItem variants={itemVariants} label="Regional Tax Invariant" status="Pending" score={82} />
          </div>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1 }}
          className="mt-auto pt-8 border-t border-surface-border"
        >
          <div className="card-premium p-6 bg-brand-primary/5 border-brand-primary/20">
            <div className="flex items-center gap-3 mb-3">
              <Bolt size={16} className="text-brand-primary" />
              <h4 className="text-xs font-black text-white uppercase tracking-widest">Agent Health</h4>
            </div>
            <div className="space-y-3">
              <div className="flex justify-between text-[10px] font-bold">
                <span className="text-text-dim">Latency</span>
                <span className="text-white">14ms</span>
              </div>
              <div className="w-full h-1 bg-surface-border rounded-full overflow-hidden">
                <div className="w-[85%] h-full bg-brand-primary shadow-[0_0_8px_#7C3AED]" />
              </div>
            </div>
          </div>
        </motion.div>
      </aside>
    </motion.div>
  );
}

function ChatMessage({ type, msg, flagged, ...props }: any) {
  return (
    <motion.div {...props} className={`flex ${type === 'user' ? 'justify-end' : 'justify-start'} group`}>
      <div className={`max-w-[75%] p-6 rounded-3xl text-sm leading-relaxed font-medium shadow-xl ${
        type === 'user' 
          ? 'bg-brand-primary text-white rounded-tr-none' 
          : `bg-surface-1 border ${flagged ? 'border-warning/50 bg-warning/5' : 'border-surface-border'} text-text-secondary rounded-tl-none`
      }`}>
        {flagged && (
          <div className="flex items-center gap-2 mb-3">
            <AlertCircle size={14} className="text-warning" />
            <span className="text-[10px] font-black text-warning uppercase tracking-widest">Manual Oversight Required</span>
          </div>
        )}
        {msg}
      </div>
    </motion.div>
  );
}

function QueueItem({ label, status, color = 'border-surface-border', score, ...props }: any) {
  return (
    <motion.div {...props} className={`p-5 rounded-2xl bg-surface-1 border ${color} hover:bg-white/5 transition-all cursor-pointer group shadow-lg`}>
      <div className="flex justify-between items-start mb-2">
        <h4 className="text-sm font-black text-white tracking-tight group-hover:text-brand-primary transition-colors">{label}</h4>
        <span className="text-[10px] font-black text-white opacity-40">{score}%</span>
      </div>
      <div className="flex items-center justify-between">
        <span className="text-[10px] font-bold text-text-dim uppercase tracking-widest">{status}</span>
        <div className="w-8 h-8 rounded-lg bg-surface-base border border-surface-border flex items-center justify-center text-text-dim hover:text-white transition-colors">
          <ChevronRight size={14} />
        </div>
      </div>
    </motion.div>
  );
}

function Brief() {
  return (
    <motion.div 
      initial="hidden"
      animate="visible"
      variants={containerVariants}
      className="max-w-5xl mx-auto space-y-24 pb-48 relative z-10"
    >
      {/* Header Section */}
      <motion.header 
        variants={itemVariants} 
        className="text-center py-16 space-y-8 relative overflow-hidden rounded-3xl"
      >
        <div className="absolute inset-0 bg-brand-primary/5 blur-[120px] rounded-full animate-pulse" />
        <div className="relative z-10 space-y-4">
          <motion.p 
            initial={{ opacity: 0, tracking: "0.5em" }}
            animate={{ opacity: 1, tracking: "0.2em" }}
            className="font-mono text-[11px] text-brand-primary uppercase font-bold"
          >
            🤖 FounderOS · Stitch Design Brief · v1.0
          </motion.p>
          <h1 className="text-6xl font-display font-black text-white leading-[0.9] tracking-tighter">
            The AI Operating System<br />
            <span className="text-brand-primary">for Solo Founders</span>
          </h1>
          <p className="text-xl text-text-secondary max-w-2xl mx-auto font-medium leading-relaxed">
            A complete feature map of FounderOS — what every page does, what every component means, what data flows through it, and exactly where Stitch should focus to make it world-class.
          </p>
        </div>
        
        <motion.div variants={containerVariants} className="flex flex-wrap justify-center gap-3 pt-6 relative z-10">
          <Badge icon={<Bot size={12} />} label="5 AI Agents" color="text-success" />
          <Badge icon={<ShieldCheck size={12} />} label="React + Vite + TS" color="text-brand-primary" />
          <Badge icon={<Bolt size={12} />} label="Tailwind + shadcn/ui" color="text-warning" />
          <Badge icon={<TrendingUp size={12} />} label="7 Routes" />
        </motion.div>
      </motion.header>

      {/* Table of Contents */}
      <motion.section variants={itemVariants} className="bg-surface-1 border border-surface-border p-10 rounded-3xl shadow-2xl relative overflow-hidden group">
        <div className="absolute top-0 right-0 w-64 h-64 bg-brand-primary/5 blur-3xl rounded-full opacity-0 group-hover:opacity-100 transition-opacity" />
        <p className="font-mono text-[10px] text-text-dim uppercase tracking-[0.2em] mb-8">Contents</p>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
          {[
            { id: "overview", num: "01", label: "Product Overview" },
            { id: "landing", num: "02", label: "Landing Sections" },
            { id: "agents", num: "03", label: "The 5 AI Agents" },
            { id: "app-pages", num: "04", label: "App Pages" },
            { id: "components", num: "05", label: "Shared Components" },
            { id: "routes", num: "06", label: "Route Map" },
            { id: "tokens", num: "07", label: "Design Tokens" },
            { id: "flux", num: "08", label: "Core UX Flow" },
            { id: "targets", num: "09", label: "Improvement Targets" },
          ].map(item => (
            <motion.a 
              key={item.id}
              href={`#${item.id}`}
              whileHover={{ x: 5, backgroundColor: "rgba(255,255,255,0.03)" }}
              className="flex items-center gap-4 p-3 rounded-xl border border-transparent hover:border-surface-border transition-all"
            >
              <span className="font-mono text-[10px] text-brand-primary font-bold">{item.num}</span>
              <span className="text-sm font-semibold text-text-secondary hover:text-white">{item.label}</span>
            </motion.a>
          ))}
        </div>
      </motion.section>

      {/* 01 Product Overview */}
      <DocSection id="overview" num="01" title="Product Overview">
        <p className="text-lg text-text-secondary leading-relaxed">
          FounderOS is a B2B SaaS product that positions itself as an "AI Operating System" for solo entrepreneurs. The premise: instead of hiring employees, a solo founder deploys 5 specialized AI agents that work overnight — scanning markets, triaging email, sourcing candidates, qualifying sales leads, and handling customer support.
        </p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-8">
          <BriefCard icon="🏗️" title="Tech Stack" body="React 18 + TypeScript, Vite, Tailwind CSS v3, shadcn/ui, Framer Motion, React Router v6, Lucide icons." />
          <BriefCard icon="📄" title="Two Surfaces" body="A public Landing Page (/) that converts visitors, and a private App (/app/*) with a sidebar layout." />
          <BriefCard icon="🎯" title="Target User" body="Solo founders / indie hackers / micro-SaaS operators who need business operations covered." />
          <BriefCard icon="💡" title="Core Value Prop" body="'5 AI agents work through the night. You wake up, review what got done, approve the good stuff.'" />
        </div>
      </DocSection>

      {/* 03 The 5 AI Agents */}
      <DocSection id="agents" num="03" title="The 5 AI Agents">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <AgentBrief icon={<TrendingUp size={24} />} num="01" name="Intel" sub="Business Intelligence" body="Scans 47+ sources per day. Delivers a daily SWOT analysis, competitor moves, market signals." metric="47 sources scanned / day" />
          <AgentBrief icon={<Mail size={24} />} num="02" name="Triage" sub="Email Assistant" body="Reads inbox overnight, drafts replies in the founder's tone, flags meeting requests." metric="92% draft approval rate" />
          <AgentBrief icon={<Users size={24} />} num="03" name="Scout" sub="Talent Sourcer" body="Finds candidates that fit, scores them 1-10, writes personalized outreach." metric="Powered by People Data Labs" />
          <AgentBrief icon={<UserSearch size={24} />} num="04" name="Qualifier" sub="Lead Closer" body="Answers the sales phone line 24/7. Qualifies leads using BANT framework." metric="Avg. 4-min discovery call" />
          <AgentBrief icon={<Bot size={24} />} num="05" name="Helper" sub="Customer Support" body="Resolves common support questions instantly via chat widget. Flags low-confidence." metric="78% auto-resolution" />
        </div>
      </DocSection>

      {/* 09 Improvement Targets */}
      <DocSection id="targets" num="09" title="Improvement Targets for Stitch">
        <div className="space-y-12">
          <div>
            <p className="font-mono text-[10px] text-error uppercase tracking-[0.2em] mb-6 flex items-center gap-2">
              <AlertCircle size={14} /> High Priority
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <TargetCard status="high" title="No Real Onboarding Flow" body="The CTA captures email but the app just opens on Dashboard. There's no setup wizard or agent configuration flow." what="Add a multi-step onboarding wizard: Connect Gmail → Configure Agents → Set ICP → Done." />
              <TargetCard status="high" title="No Notifications / Activity Feed" body="No way for the app to alert the founder to urgent items. No notification bell or real-time updates." what="Add a notification hub in AppTopbar. Add status badges on sidebar nav items." />
            </div>
          </div>

          <div>
            <p className="font-mono text-[10px] text-warning uppercase tracking-[0.2em] mb-6 flex items-center gap-2">
              <AlertCircle size={14} /> Medium Priority
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <TargetCard status="med" title="Intel Page Can't Export or Save" body="The SWOT analysis has no export button or save to history feature. Every run generates fresh results." what="Add 'Export PDF' button. Implement a 'Briefing History' panel showing past market intel runs." />
              <TargetCard status="med" title="CS Bot Interaction Gap" body="The chat input in the CS Bot page does nothing. The conversation is currently frozen mock data." what="Wire chat input to append messages. Simulate AI response using a predictive mock or LLM bridge." />
            </div>
          </div>
        </div>
      </DocSection>

      <footer className="text-center pt-24 border-t border-surface-border opacity-40">
        <p className="text-sm font-mono tracking-widest text-text-dim">FOUNDEROS TECHNICAL SPEC v1.0.0 — END OF DOCUMENT</p>
      </footer>
    </motion.div>
  );
}

function DocSection({ id, num, title, children }: any) {
  return (
    <motion.section 
      id={id} 
      variants={itemVariants} 
      initial="hidden" 
      whileInView="visible" 
      viewport={{ once: true, margin: "-100px" }}
      className="scroll-mt-32 space-y-8"
    >
      <div className="flex items-baseline gap-4 border-b border-surface-border pb-6">
        <span className="font-mono text-xs text-brand-primary font-bold tracking-widest">{num}</span>
        <h2 className="text-3xl font-display font-black text-white tracking-tight">{title}</h2>
      </div>
      <div className="space-y-6">
        {children}
      </div>
    </motion.section>
  );
}

function BriefCard({ icon, title, body }: any) {
  return (
    <div className="card-premium p-8 group">
      <div className="text-3xl mb-4 grayscale group-hover:grayscale-0 transition-all duration-500 scale-100 group-hover:scale-110 origin-left">{icon}</div>
      <h4 className="text-lg font-display font-black text-white mb-2 tracking-tight">{title}</h4>
      <p className="text-sm text-text-secondary leading-relaxed font-medium">{body}</p>
    </div>
  );
}

function AgentBrief({ icon, num, name, sub, body, metric }: any) {
  return (
    <div className="card-premium p-8 space-y-6 relative overflow-hidden group">
      <div className="flex justify-between items-start">
        <div className="w-12 h-12 rounded-xl bg-surface-2 border border-surface-border flex items-center justify-center text-brand-primary group-hover:scale-110 transition-transform">
          {icon}
        </div>
        <span className="badge-premium">Agent {num}</span>
      </div>
      <div>
        <h4 className="text-xl font-display font-black text-white tracking-tight">{name}</h4>
        <p className="text-[10px] font-mono text-text-dim uppercase tracking-widest font-bold">{sub}</p>
      </div>
      <p className="text-sm text-text-secondary leading-relaxed font-medium">{body}</p>
      <div className="pt-4 border-t border-surface-border flex items-center gap-2">
        <div className="w-1.5 h-1.5 rounded-full bg-success animate-pulse" />
        <span className="text-[10px] font-mono text-text-dim tracking-wider">{metric}</span>
      </div>
    </div>
  );
}

function TargetCard({ status, title, body, what }: any) {
  const color = status === 'high' ? 'border-error/20 bg-error/5' : 'border-warning/20 bg-warning/5';
  const labelColor = status === 'high' ? 'text-error' : 'text-warning';
  
  return (
    <div className={`p-8 rounded-3xl border ${color} space-y-6 flex flex-col h-full`}>
      <div className="space-y-2">
        <p className={`font-mono text-[9px] font-black uppercase tracking-widest ${labelColor}`}>Condition</p>
        <h4 className="text-lg font-display font-black text-white tracking-tight leading-tight">{title}</h4>
        <p className="text-sm text-text-secondary leading-relaxed font-medium opacity-80">{body}</p>
      </div>
      <div className="mt-auto pt-6 space-y-3">
        <p className="font-mono text-[9px] font-black text-white/40 uppercase tracking-widest">Execution Path</p>
        <div className="p-4 rounded-xl bg-white/5 border border-white/5">
          <p className="text-xs text-text-primary leading-relaxed font-semibold">{what}</p>
        </div>
      </div>
    </div>
  );
}

function Badge({ icon, label, color = "text-text-dim" }: any) {
  return (
    <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full bg-surface-2 border border-surface-border shadow-sm group hover:border-surface-border-light transition-all`}>
      <span className={color}>{icon}</span>
      <span className="text-[10px] font-mono font-bold uppercase tracking-widest text-text-secondary group-hover:text-white">{label}</span>
    </div>
  );
}
