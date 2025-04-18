# Atlas Frontend

This is the frontend of the **Atlas Workspace Management Platform**, built with [Next.js](https://nextjs.org) and styled using **Tailwind CSS**. The project is modular, scalable, and designed for seamless integration with backend APIs.

---

## **Getting Started**

Follow these steps to set up and run the project locally:

### **Prerequisites**
Ensure you have the following installed on your system:
- **Node.js** (v16 or later)
- **npm**, **yarn**, or **pnpm** (any package manager of your choice)

### **Installation**
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/atlas-frontend.git
   cd atlas-frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   # or
   yarn install
   # or
   pnpm install
   ```

### **Running the Development Server**
Start the development server:
```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser to view the application.

---

## **Project Setup**

This project was bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app) and uses the following key technologies:

- **Next.js**: For server-side rendering, routing, and API handling.
- **TypeScript**: For type safety and better developer experience.
- **Tailwind CSS**: For utility-first styling.
- **shadcn/ui**: For building reusable UI components.

---

## **Folder Structure**

The project follows a modular and organized folder structure:

- **`/components`**: Contains reusable UI components grouped by functionality.
  - **`/layout`**: Includes layout components like `Navbar` and `Footer`.
  - **`/sections`**: Contains page-specific sections like `Hero`, `Resources`, `Solutions`, etc.
  - **`/auth`**: Includes authentication-related components like `Login`.

- **`/app`**: Contains the main application pages and routing logic.
  - **`/page.tsx`**: The landing page that renders all the reusable sections.
  - **`/login/page.tsx`**: The dedicated login page.

- **`/public`**: Stores static assets like images and icons.

- **`/styles`**: (Optional) Can be used for global styles or Tailwind configuration.

---

## **Key Features**

### **1. Modular Design**
- The project is divided into reusable components and sections for better maintainability.
- Example sections include:
  - **Hero**: The landing page hero section with a search bar.
  - **Solutions**: Highlights integrations with tools like Slack, Google, and Microsoft.

### **2. Styling**
- Tailwind CSS is used for responsive and modern UI design.
- Utility classes make it easy to customize and extend styles.

### **3. TypeScript**
- TypeScript ensures type safety and reduces runtime errors.
- All components and pages are written in TypeScript.

### **4. Client-Side Rendering**
- Components like `Navbar` and `Footer` use React hooks and are marked with the `"use client"` directive for interactivity.

### **5. Reusable Layout**
- A shared `MainLayout` wraps all pages with a `Navbar` at the top and a `Footer` at the bottom.

---

## **How to Test**

### **Running Tests**
1. Install testing dependencies:
   ```bash
   npm install --save-dev jest @testing-library/react @testing-library/jest-dom
   ```

2. Add a test script to `package.json`:
   ```json
   "scripts": {
     "test": "jest"
   }
   ```

3. Run tests:
   ```bash
   npm test
   ```

### **Testing Features**
- Write unit tests for individual components in the `/components` folder.
- Use [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/) for testing UI interactions.

---

## **Deployment**

To deploy the application, follow these steps:

1. Build the project:
   ```bash
   npm run build
   ```

2. Start the production server:
   ```bash
   npm start
   ```

3. Alternatively, deploy to platforms like [Vercel](https://vercel.com) or [Netlify](https://www.netlify.com).

---

## **Contributing**

If you'd like to contribute:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Submit a pull request with a detailed description of your changes.

---

## **License**

This project is licensed under the MIT License. See the `LICENSE` file for details.