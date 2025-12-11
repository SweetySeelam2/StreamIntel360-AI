// frontend/app/layout.tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'StreamIntel360',
  description: 'Multi-agent content intelligence for streaming strategy',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body
        style={{
          margin: 0,
          fontFamily:
            'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
          background: '#f3f4f6', // soft gray
          color: '#0b1120',
        }}
      >
        <div
          style={{
            minHeight: '100vh',
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'flex-start', // move content closer to top
            padding: '1.5rem 1.5rem 2.5rem', // less top padding
          }}
        >
          <div
            style={{
              width: '100%',
              maxWidth: '1120px',
              background: '#ffffff',
              borderRadius: '18px',
              boxShadow:
                '0 18px 45px rgba(15, 23, 42, 0.12), 0 0 0 1px rgba(15, 23, 42, 0.04)',
              padding: '1.8rem 2.4rem 2.4rem', // slightly tighter top padding
            }}
          >
            {children}
          </div>
        </div>
      </body>
    </html>
  );
}