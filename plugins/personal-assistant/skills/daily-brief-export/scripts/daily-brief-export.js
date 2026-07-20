// api/daily-brief-export.js — Private endpoint for an AI assistant.
// Protected by API_TOKEN env var. No browser session required.

import {
  clientFromRefreshToken,
  listTodaysEvents,
  listThreads,
  listIncompleteTasks
} from '../lib/google.js';

const EMAIL_QUERY = [
  'is:unread',
  'newer_than:1d',
  '-in:draft',
  '-category:promotions',
  '-category:social'
  // add '-from:<sender>' lines for your own noisy automated senders
].join(' ');

export default async function handler(req, res) {
  const token = req.headers['x-api-token'] || req.query.token;
  if (!token || token !== process.env.API_TOKEN) {
    return res.status(401).json({ error: 'unauthorized' });
  }

  const refreshToken = process.env.GOOGLE_REFRESH_TOKEN;
  if (!refreshToken) {
    return res.status(500).json({ error: 'GOOGLE_REFRESH_TOKEN not configured' });
  }

  try {
    const client = clientFromRefreshToken(refreshToken);

    const [events, tasks, emailThreads] = await Promise.all([
      listTodaysEvents(client),
      listIncompleteTasks(client, 25).catch(() => []),
      listThreads(client, EMAIL_QUERY, 10)
    ]);

    res.json({
      date: new Date().toLocaleDateString('en-US', {
        weekday: 'long', month: 'long', day: 'numeric', year: 'numeric'
      }),
      calendar: events.map(e => ({
        time: (e.start && (e.start.dateTime || e.start.date)) || '',
        summary: e.summary || '',
        location: e.location || '',
        attendees: (e.attendees || []).map(a => a.email)
      })),
      tasks: tasks.map(t => ({
        title: t.title,
        due: t.due || null,
        notes: (t.notes || '').slice(0, 200)
      })),
      emails: emailThreads.map(t => {
        const m = (t.messages || [])[0] || {};
        return {
          from: m.sender || '',
          subject: m.subject || '',
          snippet: (m.snippet || '').slice(0, 300)
        };
      })
    });
  } catch (err) {
    console.error('daily-brief-export error', err);
    res.status(500).json({ error: 'export_failed', message: String(err.message || err) });
  }
}
