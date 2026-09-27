"use client";

import { useEffect, useRef, useState } from "react";

type Customer = {
  id: number;
  name: string;
  phone: string;
  company_name: string | null;
  purpose: string | null;
  product: string | null;
  created_at: string;
};

type Call = {
  id: number;
  customer_id: number;
  direction: string;
  status: string;
  duration: number | null;
  outcome: string | null;
  lead_status: string | null;
  follow_up_required: string;
};

const API_URL = "http://127.0.0.1:8000";

export default function Home() {
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [calls, setCalls] = useState<Call[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showAddCustomer, setShowAddCustomer] = useState(false);
  const [activeCallId, setActiveCallId] = useState<number | null>(null);
  const [mediaRecorder, setMediaRecorder] = useState<MediaRecorder | null>(null);
  const [audioChunks, setAudioChunks] = useState<Blob[]>([]);
  const [recording, setRecording] = useState(false);
  const [voiceResult, setVoiceResult] = useState("");

  const audioChunksRef = useRef<Blob[]>([]);

  const [newCustomer, setNewCustomer] = useState({
  name: "",
  phone: "",
  company_name: "",
  purpose: "",
  product: "",
});

  useEffect(() => {
    async function loadData() {
      try {
        const [customersResponse, callsResponse] = await Promise.all([
          fetch(`${API_URL}/customers`),
          fetch(`${API_URL}/calls`),
        ]);

        if (!customersResponse.ok || !callsResponse.ok) {
          throw new Error("Failed to load dashboard data");
        }

        const customersData = await customersResponse.json();
        const callsData = await callsResponse.json();

        setCustomers(customersData);
        setCalls(callsData);
      } catch (err) {
        console.error(err);
        setError(
          "Could not connect to the backend. Make sure FastAPI is running on port 8000."
        );
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, []);

  async function addCustomer() {
  try {
    const response = await fetch(`${API_URL}/customers`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(newCustomer),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Failed to create customer");
    }

    setCustomers((previous) => [data, ...previous]);

    setNewCustomer({
      name: "",
      phone: "",
      company_name: "",
      purpose: "",
      product: "",
    });

    setShowAddCustomer(false);
  } catch (err) {
    console.error(err);
    setError(
      err instanceof Error
        ? err.message
        : "Failed to create customer"
    );
  }
}

async function startCall(customerId: number) {
  try {
    const response = await fetch(`${API_URL}/calls`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        customer_id: customerId,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Failed to start call");
    }

    setCalls((previous) => [data, ...previous]);

    setActiveCallId(data.id);
  } catch (err) {
    console.error(err);

    setError(
      err instanceof Error
        ? err.message
        : "Failed to start call"
    );
  }
}

async function endCall() {
  if (activeCallId === null) {
    return;
  }

  try {
    const response = await fetch(
      `${API_URL}/calls/${activeCallId}/status?status=completed`,
      {
        method: "PATCH",
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.detail || "Failed to end call"
      );
    }

    setCalls((previous) =>
      previous.map((call) =>
        call.id === activeCallId
          ? data
          : call
      )
    );

    setActiveCallId(null);
    setVoiceResult("");
  } catch (err) {
    console.error(err);

    setVoiceResult(
      err instanceof Error
        ? err.message
        : "Failed to end call"
    );
  }
}

async function startRecording() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      audio: true,
    });

    const recorder = new MediaRecorder(stream);

    audioChunksRef.current = [];

    recorder.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunksRef.current.push(event.data);
      }
    };

    recorder.onstop = () => {
      stream.getTracks().forEach((track) => track.stop());
    };

    recorder.start();

    setMediaRecorder(recorder);
    setAudioChunks([]);
    setRecording(true);
    setVoiceResult("Recording... Speak now.");
  } catch (err) {
    console.error(err);

    setVoiceResult(
      "Microphone permission error. Please allow microphone access."
    );
  }
}

async function stopRecording() {
  if (!mediaRecorder) {
    return;
  }

  mediaRecorder.onstop = async () => {
    const stream = mediaRecorder.stream;

    stream.getTracks().forEach((track) => track.stop());

    const audioBlob = new Blob(audioChunksRef.current, {
      type: "audio/webm",
    });

    setRecording(false);
    setVoiceResult("Processing your voice...");

    const formData = new FormData();

    formData.append(
      "audio",
      audioBlob,
      "recording.webm"
    );

    try {
      const response = await fetch(
        `${API_URL}/voice/process/${activeCallId}`,
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Voice processing failed"
        );
      }

      setVoiceResult(
        `You: ${data.customer_text}\n\nAI: ${data.agent_response}`
      );

      // if (data.audio_file) {
      //   const audio = new Audio(
      //     `${API_URL}/${data.audio_file.replace(/\\/g, "/")}`
      //   );

      //   await audio.play();
      // }

      if (data.audio_file) {
        console.log("AI audio file:", data.audio_file);

        const audioUrl = `${API_URL}/${data.audio_file.replace(/\\/g, "/")}`;

        console.log("AI audio URL:", audioUrl);

        const audio = new Audio(audioUrl);

        audio.onerror = (event) => {
          console.error("Audio playback error:", event);
        };

        await audio.play();
      }
    } catch (err) {
      console.error(err);

      setVoiceResult(
        err instanceof Error
          ? err.message
          : "Voice processing failed"
      );
    }
  };

  mediaRecorder.stop();
}

  const completedCalls = calls.filter(
    (call) => call.status === "completed"
  ).length;

  const activeCalls = calls.filter(
    (call) =>
      call.status === "initiated" ||
      call.status === "in_progress"
  ).length;

  return (
    <main className="min-h-screen bg-gray-100 text-gray-900">
      {activeCallId !== null && (
        <section className="mx-auto max-w-7xl px-6 pt-8">
          <div className="rounded-xl border bg-white p-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-xl font-semibold">
                  Live AI Call
                </h2>

                <p className="mt-1 text-sm text-gray-500">
                  Call #{activeCallId}
                </p>
              </div>

              <span className="rounded-full bg-green-100 px-3 py-1 text-sm font-medium text-green-700">
                ● Call Active
              </span>
            </div>

            <div className="mt-6 rounded-lg bg-gray-50 p-5">
              <p className="text-sm text-gray-500">
                AI Calling Agent
              </p>

              <p className="mt-2 text-lg font-medium">
                Ready to talk
              </p>

              <p className="mt-2 text-sm text-gray-500">
                The live voice conversation interface will be connected here.
              </p>
              {voiceResult && (
                <div className="mt-4 whitespace-pre-line rounded-lg border bg-white p-4 text-sm">
                  {voiceResult}
                </div>
              )}
              <div className="mt-5 flex gap-3">
                <button
                  onClick={() => startRecording()}
                  className="rounded-lg bg-black px-5 py-2.5 text-sm font-medium text-white hover:bg-gray-800"
                >
                  🎤 Start Recording
                </button>

                <button
                  onClick={() => stopRecording()}
                  className="rounded-lg border px-5 py-2.5 text-sm font-medium hover:bg-gray-50"
                >
                  Stop Recording
                </button>
                <button
                  onClick={() => endCall()}
                  className="rounded-lg bg-red-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-red-700"
                >
                  End Call
                </button>
              </div>
            </div>
          </div>
        </section>
      )}
      <header className="border-b bg-white">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div>
            <h1 className="text-2xl font-bold">
              AI Calling Agent
            </h1>
            <p className="mt-1 text-sm text-gray-500">
              Admin Dashboard
            </p>
          </div>

          <div className="rounded-lg bg-green-50 px-4 py-2 text-sm font-medium text-green-700">
            ● System Online
          </div>
        </div>
      </header>

      <section className="mx-auto max-w-7xl px-6 py-8">
        {loading && (
          <div className="rounded-xl border bg-white p-6">
            Loading dashboard data...
          </div>
        )}

        {error && (
          <div className="mb-6 rounded-xl border border-red-200 bg-red-50 p-4 text-red-700">
            {error}
          </div>
        )}

        {!loading && !error && (
          <>
            <div className="grid gap-5 md:grid-cols-4">
              <StatCard
                title="Customers"
                value={customers.length}
              />

              <StatCard
                title="Total Calls"
                value={calls.length}
              />

              <StatCard
                title="Completed Calls"
                value={completedCalls}
              />

              <StatCard
                title="Active Calls"
                value={activeCalls}
              />
            </div>

            <div className="mt-8 grid gap-6 lg:grid-cols-2">
              <section className="rounded-xl border bg-white p-6">
                <div className="mb-5 flex items-center justify-between">
                  <div>
                    <h2 className="text-lg font-semibold">
                      Customers
                    </h2>
                    <p className="text-sm text-gray-500">
                      Customer records from the database
                    </p>
                  </div>

                  <button
                    onClick={() => setShowAddCustomer(true)}
                    className="rounded-lg bg-black px-4 py-2 text-sm font-medium text-white hover:bg-gray-800"
                  >
                     + Add Customer
                  </button>
                </div>

                {showAddCustomer && (
                <div className="mb-5 rounded-lg border bg-gray-50 p-5">
                  <h3 className="mb-4 font-semibold">Add Customer</h3>

                  <div className="grid gap-3">
                      <input
                        type="text"
                        placeholder="Customer name"
                        value={newCustomer.name}
                        onChange={(e) =>
                          setNewCustomer({
                            ...newCustomer,
                            name: e.target.value,
                          })
                        }
                        className="rounded-lg border bg-white px-3 py-2"
                      />

                      <input
                        type="text"
                        placeholder="Phone number"
                        value={newCustomer.phone}
                        onChange={(e) =>
                          setNewCustomer({
                            ...newCustomer,
                            phone: e.target.value,
                          })
                        }
                        className="rounded-lg border bg-white px-3 py-2"
                      />
                      <input
                        type="text"
                        placeholder="Company name"
                        value={newCustomer.company_name}
                        onChange={(e) =>
                          setNewCustomer({
                            ...newCustomer,
                            company_name: e.target.value,
                          })
                        }
                        className="rounded-lg border bg-white px-3 py-2"
                      />

                      <input
                        type="text"
                        placeholder="Purpose"
                        value={newCustomer.purpose}
                        onChange={(e) =>
                          setNewCustomer({
                            ...newCustomer,
                            purpose: e.target.value,
                          })
                        }
                        className="rounded-lg border bg-white px-3 py-2"
                      />

                      <input
                        type="text"
                        placeholder="Product"
                        value={newCustomer.product}
                        onChange={(e) =>
                          setNewCustomer({
                            ...newCustomer,
                            product: e.target.value,
                          })
                        }
                        className="rounded-lg border bg-white px-3 py-2"
                      />

                      <div className="flex gap-2">
                        <button
                          onClick={addCustomer}
                          className="rounded-lg bg-black px-4 py-2 text-sm font-medium text-white"
                        >
                          Save Customer
                        </button>

                        <button
                          onClick={() => setShowAddCustomer(false)}
                          className="rounded-lg border px-4 py-2 text-sm"
                        >
                          Cancel
                        </button>
                      </div>
                    </div>
                  </div>
                )}

                {customers.length === 0 ? (
                  <p className="text-sm text-gray-500">
                    No customers found.
                  </p>
                ) : (
                  <div className="space-y-3">
                    {customers.map((customer) => (
                      <div
                        key={customer.id}
                        className="rounded-lg border p-4"
                      >
                        <div className="flex items-center justify-between">
                          <div>
                            <p className="font-semibold">
                              {customer.name}
                            </p>

                            <p className="text-sm text-gray-500">
                              {customer.company_name || "No company"}
                            </p>
                          </div>

                          <span className="rounded-full bg-gray-100 px-3 py-1 text-xs">
                            ID #{customer.id}
                          </span>
                        </div>

                        <div className="mt-3 text-sm text-gray-600">
                          <p>📞 {customer.phone}</p>

                          <p className="mt-1">
                            Product:{" "}
                            {customer.product || "Not specified"}
                          </p>
                          <button
                            onClick={() => startCall(customer.id)}
                            className="mt-3 rounded-lg bg-black px-4 py-2 text-sm font-medium text-white hover:bg-gray-800"
                          >
                            Start Call
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </section>

              <section className="rounded-xl border bg-white p-6">
                <div className="mb-5">
                  <h2 className="text-lg font-semibold">
                    Recent Calls
                  </h2>

                  <p className="text-sm text-gray-500">
                    Latest calling activity
                  </p>
                </div>

                {calls.length === 0 ? (
                  <p className="text-sm text-gray-500">
                    No calls found.
                  </p>
                ) : (
                  <div className="space-y-3">
                    {calls.slice(0, 10).map((call) => (
                      <div
                        key={call.id}
                        className="rounded-lg border p-4"
                      >
                        <div className="flex items-center justify-between">
                          <div>
                            <p className="font-semibold">
                              Call #{call.id}
                            </p>

                            <p className="text-sm text-gray-500">
                              Customer #{call.customer_id}
                            </p>
                          </div>

                          <StatusBadge status={call.status} />
                        </div>

                        <div className="mt-3 text-sm text-gray-600">
                          <p>
                            Direction: {call.direction}
                          </p>

                          <p>
                            Duration:{" "}
                            {call.duration !== null
                              ? `${call.duration}s`
                              : "—"}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </section>
            </div>
          </>
        )}
      </section>
    </main>
  );
}

function StatCard({
  title,
  value,
}: {
  title: string;
  value: number;
}) {
  return (
    <div className="rounded-xl border bg-white p-6">
      <p className="text-sm text-gray-500">{title}</p>
      <p className="mt-2 text-3xl font-bold">{value}</p>
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const statusClass =
    status === "completed"
      ? "bg-green-100 text-green-700"
      : status === "failed"
      ? "bg-red-100 text-red-700"
      : "bg-yellow-100 text-yellow-700";

  return (
    <span
      className={`rounded-full px-3 py-1 text-xs font-medium ${statusClass}`}
    >
      {status}
    </span>
  );
}