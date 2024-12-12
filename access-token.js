const { OAuth2Client } = require('google-auth-library');
const http = require('http');
const url = require('url');
const destroyer = require('server-destroy');

const clientId = '';
const clientSecret = '';
const redirectUri = 'http://localhost:3000/oauth2callback';

const oauth2Client = new OAuth2Client(clientId, clientSecret, redirectUri);

const scopes = [
  'https://www.googleapis.com/auth/spreadsheets',
  'https://www.googleapis.com/auth/youtube.force-ssl'
];

async function getAuthenticatedClient() {
  return new Promise((resolve, reject) => {
    const authorizeUrl = oauth2Client.generateAuthUrl({
      access_type: 'offline',
      scope: scopes.join(' '),
    });

    const server = http
      .createServer(async (req, res) => {
        try {
          if (req.url.indexOf('/oauth2callback') > -1) {
            const qs = new url.URL(req.url, 'http://localhost:3000')
              .searchParams;
            const code = qs.get('code');
            res.end('Authentication successful! Please return to the console.');
            server.destroy();

            const { tokens } = await oauth2Client.getToken(code);
            oauth2Client.setCredentials(tokens);
            resolve(oauth2Client);
          }
        } catch (e) {
          reject(e);
        }
      })
      .listen(3000, async () => {
        // 動的にimportを使用
        const open = await import('open');
        open.default(authorizeUrl, { wait: false }).then(cp => cp.unref());
      });
    destroyer(server);
  });
}

async function main() {
  const client = await getAuthenticatedClient();
  console.log('Access token:', client.credentials.access_token);
  console.log('Refresh token:', client.credentials.refresh_token);
}

main().catch(console.error);