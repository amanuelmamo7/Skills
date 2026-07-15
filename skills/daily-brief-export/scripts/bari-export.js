// api/bari-export.js — Private endpoint for Bari (AI assistant).
// Protected by BARI_TOKEN env var. No browser session required.

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
  '-category:social',
  '-from:no-reply@t.mail.coursera.org',
  '-from:USPSInformeddelivery@email.informeddelivery.usps.com',
  '-from:no-reply@packageconcierge.com',
  '-from:no-reply@accounts.google.com',
  '-from:googlealerts-noreply@google.com',
  '-from:jobs-noreply@linkedin.com',
  '-from:messages-noreply@linkedin.com'
].join(' ');

export default async function handler(req, res) {
  const token = req.headers['x-bari-token'] || req.query.token;
  if (!token || token !== process.env.BARI_TOKEN) {
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
    console.error('bari-export error', err);
    res.status(500).json({ error: 'export_failed', message: String(err.message || err) });
  }
}
