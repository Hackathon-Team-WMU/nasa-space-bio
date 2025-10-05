# Frontend Setup

## Prerequisites

- [Node.js](https://nodejs.org/) installed on your machine

## Installation

1. Install dependencies:
   ```bash
   npm i
   ```

2. Create a `.env` file in the frontend directory with the following variables:
   ```
   VITE_SUPABASE_PROJECT_ID=
   VITE_SUPABASE_PUBLISHABLE_KEY=
   VITE_SUPABASE_URL=
   ```

3. Fill in your Supabase credentials in the `.env` file (get them from your [Supabase project dashboard](https://supabase.com/dashboard))

## Running the Development Server

Start the development server:
```bash
npm run dev
```

The application will be accessible at [http://localhost:8080](http://localhost:8080)