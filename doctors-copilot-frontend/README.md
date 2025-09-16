# Doctor's Copilot - Frontend

A modern, responsive web application for healthcare professionals to view and analyze patient insights from the MIMIC-III dataset.

## Features

- **Secure Authentication**: Token-based authentication system
- **Patient Insights**: View detailed patient information including vitals, lab results, and risk assessments
- **Responsive Design**: Works on desktop and tablet devices
- **Real-time Updates**: Refresh data with a single click
- **Risk Assessment**: Visual indicators for patient risk levels
- **Comprehensive Patient Data**: View admission details, vital signs, lab results, and clinical assessments

## Prerequisites

- Node.js (v14 or higher)
- npm (v7 or higher) or yarn
- Backend API server (see [backend documentation](../README.md))

## Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/doctors-copilot.git
   cd doctors-copilot/doctors-copilot-frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Set up environment variables**
   - Copy `.env.example` to `.env`
   - Update the environment variables as needed

4. **Start the development server**
   ```bash
   npm start
   # or
   yarn start
   ```
   The application will be available at [http://localhost:3000](http://localhost:3000)

## Available Scripts

In the project directory, you can run:

### `npm start` or `yarn start`

Runs the app in development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test` or `yarn test`

Launches the test runner in interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build` or `yarn build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

## Project Structure

```
src/
├── components/           # Reusable UI components
├── contexts/            # React context providers
├── pages/               # Page components
├── services/            # API services and utilities
├── App.js               # Main application component
└── index.js             # Application entry point
```

## Authentication

The application uses token-based authentication. To log in, use the following default credentials:

- **Username**: admin
- **Password**: admin123

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```
REACT_APP_API_BASE_URL=http://localhost:5000
REACT_APP_API_TIMEOUT=10000
```

## API Integration

The frontend communicates with the backend API for data retrieval and authentication. Ensure the backend server is running and properly configured.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## Acknowledgments

- [MIMIC-III](https://mimic.physionet.org/) - The Medical Information Mart for Intensive Care III database
- [Ant Design](https://ant.design/) - A design system for enterprise-level products
- [React](https://reactjs.org/) - A JavaScript library for building user interfaces

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)
