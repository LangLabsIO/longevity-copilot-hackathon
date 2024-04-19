/**
 * v0 by Vercel.
 * @see https://v0.dev/t/7DkFlDT7HwZ
 * Documentation: https://v0.dev/docs#integrating-generated-code-into-your-nextjs-app
 */
export default function UserPopup() {
  return (
    <div className="max-w-md mx-auto p-4 bg-slate-800 rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-4 text-white">User Profile</h2>
      <div className="mb-4">
        <label className="block text-gray-100 font-semibold mb-2" htmlFor="age">
          Age
        </label>
        <select
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          id="age"
        >
          <option value="">Select your age</option>
          <option value="18-25">18-25</option>
          <option value="26-35">26-35</option>
          <option value="36-45">36-45</option>
          <option value="46-55">46-55</option>
          <option value="56+">56+</option>
        </select>
      </div>
      <div className="mb-4">
        <label className="block text-gray-100 font-semibold mb-2">
          Health Conditions
        </label>
        <div className="flex items-center mb-2">
          <input
            className="mr-2 focus:ring-blue-500"
            id="hypertension"
            type="checkbox"
          />
          <label className="text-gray-100" htmlFor="hypertension">
            Hypertension
          </label>
        </div>
        <div className="flex items-center mb-2">
          <input
            className="mr-2 focus:ring-blue-500"
            id="diabetes"
            type="checkbox"
          />
          <label className="text-gray-100" htmlFor="diabetes">
            Diabetes
          </label>
        </div>
        <div className="flex items-center mb-2">
          <input
            className="mr-2 focus:ring-blue-500"
            id="other-condition"
            type="checkbox"
          />
          <label className="text-gray-100" htmlFor="other-condition">
            Other
          </label>
        </div>
      </div>
      <div className="mb-4">
        <label className="block text-gray-100 font-semibold mb-2">
          Lifestyle Preferences
        </label>
        <div className="flex items-center mb-2">
          <input
            className="mr-2 focus:ring-blue-500"
            id="vegetarian"
            type="checkbox"
          />
          <label className="text-gray-100" htmlFor="vegetarian">
            Vegetarian
          </label>
        </div>
        <div className="flex items-center mb-2">
          <input
            className="mr-2 focus:ring-blue-500"
            id="enjoys-walking"
            type="checkbox"
          />
          <label className="text-gray-100" htmlFor="enjoys-walking">
            Enjoys Walking
          </label>
        </div>
        <div className="flex items-center mb-2">
          <input
            className="mr-2 focus:ring-blue-500"
            id="other-preference"
            type="checkbox"
          />
          <label className="text-gray-100" htmlFor="other-preference">
            Other
          </label>
        </div>
      </div>
      <div className="mb-4">
        <label className="block text-gray-100 font-semibold mb-2">
          Health Goals
        </label>
        <div className="flex items-center mb-2">
          <input
            className="mr-2 focus:ring-blue-500"
            id="reduce-blood-pressure"
            type="checkbox"
          />
          <label className="text-gray-100" htmlFor="reduce-blood-pressure">
            Reduce Blood Pressure
          </label>
        </div>
        <div className="flex items-center mb-2">
          <input
            className="mr-2 focus:ring-blue-500"
            id="manage-blood-sugar"
            type="checkbox"
          />
          <label className="text-gray-100" htmlFor="manage-blood-sugar">
            Manage Blood Sugar
          </label>
        </div>
        <div className="flex items-center mb-2">
          <input
            className="mr-2 focus:ring-blue-500"
            id="other-goal"
            type="checkbox"
          />
          <label className="text-gray-100" htmlFor="other-goal">
            Other
          </label>
        </div>
      </div>
    </div>
  );
}
