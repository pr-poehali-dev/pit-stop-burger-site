const Index = () => {
  return (
    <div className="min-h-screen bg-background text-foreground relative overflow-hidden">
      <div 
        className="absolute left-0 top-0 w-[500px] h-[500px] bg-cover bg-center opacity-90"
        style={{
          backgroundImage: "url('https://cdn.poehali.dev/projects/b69e69c0-67e8-4990-8ea3-89b409ce2aa3/files/802d38fe-f182-4f47-a714-2aaa19552443.jpg')"
        }}
      />
      
      <h1 className="absolute left-8 bottom-[calc(100vh-520px)] text-4xl font-heading font-bold animate-fade-in z-20">
        ПИТ СТОП БУРГЕР
      </h1>

      <div className="absolute right-8 top-8 z-20">
        <h2 className="text-5xl font-heading font-bold tracking-wider">
          МЕНЮ
        </h2>
      </div>
    </div>
  );
};

export default Index;